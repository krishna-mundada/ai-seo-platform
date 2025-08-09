import openai
from anthropic import Anthropic
import ollama
import httpx
from typing import Dict, Any, List, Optional
from app.core.config import settings
from app.models.content import ContentType, ContentStatus
from app.models.business import Business
import json

class AIContentService:
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self.ollama_available = False
        
        if settings.openai_api_key:
            openai.api_key = settings.openai_api_key
            self.openai_client = openai
        
        if settings.anthropic_api_key:
            self.anthropic_client = Anthropic(api_key=settings.anthropic_api_key)
        
        # Check if Ollama is available (local development only)
        self.ollama_available = self._check_ollama_availability()
    
    async def generate_content(
        self, 
        business: Business, 
        content_type: ContentType,
        topic: Optional[str] = None,
        keywords: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Generate AI content based on business context"""
        
        # Build prompt based on content type and business context
        prompt = self._build_prompt(business, content_type, topic, keywords)
        
        # Generate content using available AI service
        content_text = await self._generate_with_ai(prompt, content_type)
        
        # Generate SEO metadata
        seo_data = await self._generate_seo_metadata(content_text, keywords)
        
        return {
            "title": seo_data.get("title", topic or "Generated Content"),
            "content_text": content_text,
            "content_type": content_type,
            "business_id": business.id,
            "status": ContentStatus.PENDING_APPROVAL,
            "meta_description": seo_data.get("meta_description"),
            "keywords": keywords or seo_data.get("keywords", []),
            "seo_score": seo_data.get("seo_score", 0),
            "ai_prompt_used": prompt,
            "ai_model_used": self._get_model_name(),
            "generation_settings": {
                "temperature": 0.7,
                "max_tokens": self._get_max_tokens(content_type)
            },
            "is_auto_generated": True,
            "requires_approval": True
        }
    
    def _build_prompt(
        self, 
        business: Business, 
        content_type: ContentType, 
        topic: Optional[str] = None,
        keywords: Optional[List[str]] = None
    ) -> str:
        """Build AI prompt based on business context and content type"""
        
        base_context = f"""
Business Context:
- Company: {business.name}
- Industry: {business.industry or 'Not specified'}
- Description: {business.description or 'Not specified'}
- Target Audience: {business.target_audience or 'General audience'}
- Brand Voice: {business.brand_voice or 'Professional and engaging'}
- Website: {business.website_url or 'Not specified'}
"""
        
        if keywords:
            base_context += f"\n- Target Keywords: {', '.join(keywords)}"
        
        content_prompts = {
            ContentType.BLOG_POST: f"""
Write a comprehensive blog post for this business.
{f"Topic: {topic}" if topic else "Choose an engaging topic relevant to their industry."}

Requirements:
- 1000-1500 words
- SEO optimized with target keywords naturally integrated
- Include engaging headline and meta description
- Structure with clear headings and subheadings
- Professional tone matching the brand voice
- Include actionable insights for the target audience
- End with a call-to-action

Format as markdown with proper headings.
""",
            
            ContentType.LINKEDIN_POST: f"""
Create a LinkedIn post for this business.
{f"Topic: {topic}" if topic else "Choose a topic that showcases industry expertise."}

Requirements:
- 200-300 words maximum
- Professional tone suitable for LinkedIn
- Include relevant hashtags (3-5)
- Encourage engagement with a question or call-to-action
- Match the brand voice
- Share valuable insights or industry knowledge
""",
            
            ContentType.TWITTER_POST: f"""
Create a Twitter/X post for this business.
{f"Topic: {topic}" if topic else "Choose a trending or relevant topic."}

Requirements:
- Under 280 characters
- Include 1-3 relevant hashtags
- Engaging and shareable
- Match the brand voice
- Include a clear call-to-action if appropriate
""",
            
            ContentType.FACEBOOK_POST: f"""
Create a Facebook post for this business.
{f"Topic: {topic}" if topic else "Choose an engaging topic for Facebook audience."}

Requirements:
- 100-200 words
- Conversational and engaging tone
- Include call-to-action
- Suitable for Facebook audience
- Match the brand voice
- Encourage likes, comments, and shares
""",
            
            ContentType.INSTAGRAM_POST: f"""
Create an Instagram post caption for this business.
{f"Topic: {topic}" if topic else "Choose a visually appealing topic."}

Requirements:
- 150-300 words
- Instagram-friendly tone (casual but professional)
- Include relevant hashtags (8-15)
- Engaging caption that complements visual content
- Call-to-action appropriate for Instagram
- Match the brand voice
"""
        }
        
        return base_context + "\n" + content_prompts.get(content_type, content_prompts[ContentType.BLOG_POST])
    
    async def _generate_with_ai(self, prompt: str, content_type: ContentType) -> str:
        """Generate content using available AI service"""
        max_tokens = self._get_max_tokens(content_type)
        
        try:
            # Environment-based priority:
            # Local development: Ollama -> Mock
            # Deployed environments: Anthropic -> OpenAI -> Mock
            
            if settings.environment == "development" and self.ollama_available:
                response = await self._generate_with_ollama(prompt, max_tokens, content_type)
            elif self.anthropic_client:
                response = await self._generate_with_anthropic(prompt, max_tokens)
            elif self.openai_client:
                response = await self._generate_with_openai(prompt, max_tokens)
            else:
                # Fallback mock content 
                return self._generate_mock_content(content_type)
            
            return response
        except Exception as e:
            print(f"AI generation error: {e}")
            return self._generate_mock_content(content_type)
    
    def _get_model_name(self) -> str:
        """Get the name of the AI model being used"""
        if settings.environment == "development" and self.ollama_available:
            return f"ollama-{settings.ollama_default_model}"
        elif self.anthropic_client:
            return "anthropic-claude"
        elif self.openai_client:
            return "openai-gpt-4"
        else:
            return "mock-content"
    
    async def _generate_with_openai(self, prompt: str, max_tokens: int) -> str:
        """Generate content using OpenAI"""
        response = await self.openai_client.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message.content
    
    async def _generate_with_anthropic(self, prompt: str, max_tokens: int) -> str:
        """Generate content using Anthropic Claude"""
        response = await self.anthropic_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=max_tokens,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    
    def _generate_mock_content(self, content_type: ContentType) -> str:
        """Generate mock content for development/testing"""
        mock_content = {
            ContentType.BLOG_POST: """# The Future of Digital Marketing: Trends to Watch in 2024

Digital marketing continues to evolve at a rapid pace, and businesses that want to stay competitive must adapt to the latest trends and technologies. In this comprehensive guide, we'll explore the key trends shaping the digital marketing landscape in 2024.

## 1. AI-Powered Personalization

Artificial intelligence is revolutionizing how businesses interact with their customers. By leveraging AI algorithms, companies can now deliver highly personalized experiences at scale.

## 2. Voice Search Optimization

With the growing popularity of voice assistants, optimizing for voice search has become crucial for businesses looking to maintain their online visibility.

## 3. Interactive Content

Interactive content such as polls, quizzes, and augmented reality experiences are becoming increasingly important for engaging modern audiences.

## Conclusion

The digital marketing landscape continues to evolve, and businesses must stay ahead of these trends to remain competitive. By embracing AI, optimizing for voice search, and creating interactive content, your business can thrive in the digital age.

Ready to transform your digital marketing strategy? Contact us today to learn how we can help your business succeed online.""",
            
            ContentType.LINKEDIN_POST: """🚀 The digital marketing landscape is evolving faster than ever! 

As we move into 2024, three key trends are reshaping how businesses connect with their audiences:

✅ AI-powered personalization is enabling hyper-targeted campaigns
✅ Voice search optimization is becoming essential for visibility  
✅ Interactive content is driving unprecedented engagement rates

Companies that embrace these trends early will have a significant competitive advantage.

What digital marketing trend are you most excited about? Share your thoughts below! 👇

#DigitalMarketing #AI #Innovation #MarketingTrends #BusinessGrowth""",
            
            ContentType.TWITTER_POST: "🔥 AI is transforming digital marketing in 2024! From personalized campaigns to voice search optimization, businesses are seeing incredible results. What's your favorite AI marketing tool? #AIMarketing #DigitalTransformation #MarketingTech",
            
            ContentType.FACEBOOK_POST: """Did you know that 75% of consumers expect personalized experiences from brands? 🎯

The future of marketing is here, and it's powered by AI! Businesses using artificial intelligence for personalization are seeing:

• 20% increase in customer satisfaction
• 15% boost in conversion rates  
• 30% improvement in customer retention

Ready to join the AI revolution? We're here to help you transform your marketing strategy and deliver the personalized experiences your customers crave.

What questions do you have about AI in marketing? Drop them in the comments! 👇""",
            
            ContentType.INSTAGRAM_POST: """✨ Marketing magic happens when technology meets creativity! 

We're obsessed with how AI is transforming the way brands connect with their audience. From personalized content to predictive analytics, the possibilities are endless! 

Swipe to see our favorite AI marketing tools that are changing the game in 2024 ➡️

Which one would you try first? Tell us in the comments! 

#AIMarketing #DigitalInnovation #MarketingTech #BusinessGrowth #ContentStrategy #MarketingTips #TechTrends #AITools #DigitalTransformation #MarketingMagic #Innovation #FutureOfMarketing #BusinessSuccess #ContentCreation #MarketingStrategy"""
        }
        
        return mock_content.get(content_type, "Generated content placeholder")
    
    def _get_max_tokens(self, content_type: ContentType) -> int:
        """Get appropriate max tokens based on content type"""
        token_limits = {
            ContentType.BLOG_POST: 2000,
            ContentType.LINKEDIN_POST: 400,
            ContentType.TWITTER_POST: 100,
            ContentType.FACEBOOK_POST: 300,
            ContentType.INSTAGRAM_POST: 400,
            ContentType.REDDIT_POST: 500,
            ContentType.QUORA_POST: 800,
            ContentType.EMAIL: 1000,
            ContentType.AD_COPY: 200
        }
        return token_limits.get(content_type, 500)
    
    async def _generate_seo_metadata(self, content: str, target_keywords: Optional[List[str]] = None) -> Dict[str, Any]:
        """Generate SEO metadata for content"""
        
        # Extract title from content (first line or heading)
        lines = content.strip().split('\n')
        title = lines[0].replace('#', '').strip() if lines else "Generated Content"
        
        # Generate meta description (first paragraph or truncated content)
        meta_description = ""
        for line in lines[1:]:
            if line.strip() and not line.startswith('#'):
                meta_description = line.strip()[:155] + "..."
                break
        
        # Basic SEO score calculation (mock implementation)
        seo_score = 70
        if target_keywords:
            for keyword in target_keywords:
                if keyword.lower() in content.lower():
                    seo_score += 5
        
        seo_score = min(seo_score, 100)
        
        return {
            "title": title,
            "meta_description": meta_description,
            "keywords": target_keywords or [],
            "seo_score": seo_score
        }
    
    def _check_ollama_availability(self) -> bool:
        """Check if Ollama is available and has the required model (local development only)"""
        # Only check Ollama in development environment
        if settings.environment != "development":
            print("🚀 Production environment - Skipping Ollama (using cloud APIs)")
            return False
            
        try:
            import httpx
            response = httpx.get(f"{settings.ollama_base_url}/api/tags", timeout=2.0)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [model["name"] for model in models]
                # Check if our default model is available
                if settings.ollama_default_model in model_names:
                    print(f"✅ Ollama available with model: {settings.ollama_default_model}")
                    return True
                else:
                    print(f"⚠️  Ollama available but model {settings.ollama_default_model} not found. Available models: {model_names}")
                    print("💡 Available models:", model_names)
                    # Return True anyway if any model is available - fallback logic will handle it
                    return len(model_names) > 0
            return False
        except Exception as e:
            print(f"❌ Ollama not available (local development): {e}")
            print("💡 Install Ollama: https://ollama.ai/download")
            return False
    
    async def _generate_with_ollama(self, prompt: str, max_tokens: int, content_type: ContentType) -> str:
        """Generate content using Ollama with intelligent model selection"""
        try:
            import ollama
            
            # Configure the client to use the correct host
            client = ollama.Client(host=settings.ollama_base_url)
            
            # Select the best model for this content type
            selected_model = self._select_ollama_model(content_type)
            print(f"🎯 Using model: {selected_model} for {content_type.value}")
            
            # Create a more focused prompt for Ollama, especially reasoning models
            system_prompt = """You are a professional content writer specializing in SEO and digital marketing. 

IMPORTANT: Output ONLY the final content - no explanations, no reasoning, no thinking process, no meta-commentary.

For Twitter posts: Provide only the tweet text with hashtags.
For blog posts: Provide only the article content with headings.
For social media: Provide only the post content.

Do not include phrases like:
- "I need to create..."
- "First, I'll..."
- "The content should..."
- "Here's the content..."

Just provide the clean, final content that can be used directly."""
            
            response = client.chat(
                model=selected_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                options={
                    "num_predict": max_tokens,
                    "temperature": 0.7,
                    "top_p": 0.9,
                }
            )
            
            content = response['message']['content']
            
            # Handle reasoning models like DeepSeek-R1 that include <think> tags
            if '<think>' in content:
                # Find the end of reasoning and extract the actual content
                if '</think>' in content:
                    content = content.split('</think>')[-1].strip()
                else:
                    # If no closing tag, try to extract content after <think>
                    content = content.split('<think>')[-1].strip()
            
            # Clean up any remaining reasoning artifacts
            content = content.replace('<think>', '').replace('</think>', '').strip()
            
            return content
            
        except Exception as e:
            print(f"Ollama generation error: {e}")
            raise e
    
    def _select_ollama_model(self, content_type: ContentType) -> str:
        """Select the best Ollama model for the given content type"""
        # Map content types to model preferences
        content_type_map = {
            ContentType.BLOG_POST: "blog_post",
            ContentType.LINKEDIN_POST: "social_media", 
            ContentType.TWITTER_POST: "social_media",
            ContentType.FACEBOOK_POST: "social_media",
            ContentType.INSTAGRAM_POST: "creative",
            ContentType.REDDIT_POST: "social_media",
            ContentType.QUORA_POST: "social_media",
            ContentType.EMAIL: "creative",
            ContentType.AD_COPY: "creative"
        }
        
        # Get the model preference for this content type
        model_key = content_type_map.get(content_type, "default")
        selected_model = settings.ollama_models.get(model_key, settings.ollama_default_model)
        
        # Check if the selected model is available, fallback to available ones
        available_models = self._get_available_ollama_models()
        
        if selected_model in available_models:
            return selected_model
        
        # Fallback hierarchy: default -> fast -> any available
        fallback_order = ["default", "fast", "reasoning"]
        for fallback_key in fallback_order:
            fallback_model = settings.ollama_models.get(fallback_key)
            if fallback_model and fallback_model in available_models:
                print(f"⚠️  Preferred model {selected_model} not found, using {fallback_model}")
                return fallback_model
        
        # Last resort: use the first available model
        if available_models:
            print(f"⚠️  Using first available model: {available_models[0]}")
            return available_models[0]
        
        # Should not happen if ollama_available is True
        raise Exception("No Ollama models available")
    
    def _get_available_ollama_models(self) -> list:
        """Get list of currently available Ollama models"""
        try:
            import httpx
            response = httpx.get(f"{settings.ollama_base_url}/api/tags", timeout=2.0)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [model["name"] for model in models]
            return []
        except Exception:
            return []
    
    async def generate_topic_suggestions(
        self, 
        business: Business, 
        content_type: str, 
        category: Optional[str] = None,
        description: Optional[str] = None
    ) -> List[str]:
        """Generate AI-powered topic suggestions using existing Ollama infrastructure"""
        try:
            # Build context prompt
            context = f"""
Business: {business.name}
Industry: {business.industry or 'General Business'}
Content Type: {content_type}
"""
            
            if category:
                context += f"Category: {category}\n"
            
            if description:
                context += f"Additional Context: {description}\n"
            
            if business.description:
                context += f"Business Description: {business.description}\n"
                
            if business.target_audience:
                context += f"Target Audience: {business.target_audience}\n"

            prompt = f"""
{context}

Generate 5 engaging and relevant topic suggestions for the above context.

Requirements:
- Topics should be specific and actionable
- Match the content type format (blog post = longer topics, social media = shorter/catchier)
- Be relevant to the business and industry
- Include variety in angles and approaches
- Make them engaging and click-worthy

Return ONLY a simple numbered list of 5 topics, nothing else:
1. [Topic 1]
2. [Topic 2]
3. [Topic 3]
4. [Topic 4]
5. [Topic 5]
"""

            # Use existing AI generation infrastructure
            if settings.environment == "development" and self.ollama_available:
                response = await self._generate_suggestions_with_ollama(prompt, "topics")
            else:
                # Fallback for non-development environments
                response = self._generate_fallback_topics(business, content_type, category)
                return response
            
            # Parse response into list
            suggestions = self._parse_numbered_list(response)
            return suggestions[:5] if suggestions else self._generate_fallback_topics(business, content_type, category)
            
        except Exception as e:
            print(f"Error generating topic suggestions: {e}")
            return self._generate_fallback_topics(business, content_type, category)

    async def generate_keyword_suggestions(
        self, 
        business: Business, 
        content_type: str, 
        category: Optional[str] = None,
        topic: Optional[str] = None,
        description: Optional[str] = None
    ) -> List[str]:
        """Generate AI-powered keyword suggestions using existing Ollama infrastructure"""
        try:
            # Build context prompt
            context = f"""
Business: {business.name}
Industry: {business.industry or 'General Business'}
Content Type: {content_type}
"""
            
            if category:
                context += f"Category: {category}\n"
                
            if topic:
                context += f"Topic: {topic}\n"
            
            if description:
                context += f"Additional Context: {description}\n"
            
            if business.description:
                context += f"Business Description: {business.description}\n"
                
            if business.target_audience:
                context += f"Target Audience: {business.target_audience}\n"

            prompt = f"""
{context}

Generate 10 relevant SEO keywords/phrases for the above context.

Requirements:
- Mix of short-tail (1-2 words) and long-tail (3-5 words) keywords
- Include industry-specific terms
- Consider search intent and relevance
- Include business/brand-related keywords
- Make them SEO-friendly and searchable
- Avoid duplicates
- Focus on keywords that would help this content rank well

Return ONLY a simple numbered list of 10 keywords, nothing else:
1. [keyword1]
2. [long tail keyword]
3. [another keyword]
...
10. [final keyword]
"""

            # Use existing AI generation infrastructure
            if settings.environment == "development" and self.ollama_available:
                response = await self._generate_suggestions_with_ollama(prompt, "keywords")
            else:
                # Fallback for non-development environments
                response = self._generate_fallback_keywords(business, content_type, category)
                return response
            
            # Parse response into list
            suggestions = self._parse_numbered_list(response)
            return suggestions[:10] if suggestions else self._generate_fallback_keywords(business, content_type, category)
            
        except Exception as e:
            print(f"Error generating keyword suggestions: {e}")
            return self._generate_fallback_keywords(business, content_type, category)

    async def _generate_suggestions_with_ollama(self, prompt: str, suggestion_type: str) -> str:
        """Generate suggestions using Ollama with the existing infrastructure"""
        try:
            import ollama
            
            # Configure the client to use the correct host
            client = ollama.Client(host=settings.ollama_base_url)
            
            # Use a fast model for suggestions
            selected_model = settings.ollama_models.get("fast", settings.ollama_default_model)
            print(f"🎯 Using model: {selected_model} for {suggestion_type} suggestions")
            
            system_prompt = """You are a content marketing and SEO expert. 

IMPORTANT: Output ONLY the requested numbered list - no explanations, no reasoning, no meta-commentary.

For topic suggestions: Provide only the numbered list of topics.
For keyword suggestions: Provide only the numbered list of keywords.

Do not include phrases like:
- "Here are some suggestions..."
- "Based on the context..."
- "I would recommend..."

Just provide the clean, numbered list."""
            
            response = client.chat(
                model=selected_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                options={
                    "num_predict": 300,  # Shorter for suggestions
                    "temperature": 0.8,  # More creative for suggestions
                    "top_p": 0.9,
                }
            )
            
            content = response['message']['content']
            
            # Handle reasoning models that include <think> tags
            if '<think>' in content:
                if '</think>' in content:
                    content = content.split('</think>')[-1].strip()
                else:
                    content = content.split('<think>')[-1].strip()
            
            # Clean up any remaining reasoning artifacts
            content = content.replace('<think>', '').replace('</think>', '').strip()
            
            return content
            
        except Exception as e:
            print(f"Ollama suggestion generation error: {e}")
            raise e

    def _parse_numbered_list(self, response: str) -> List[str]:
        """Parse numbered list from AI response"""
        suggestions = []
        lines = response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            # Match patterns like "1. Topic", "1) Topic", or "1 - Topic"
            if line and any(char.isdigit() for char in line[:3]):
                # Remove numbering and clean up
                cleaned = line
                # Remove various numbering patterns
                for pattern in ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.',
                               '1)', '2)', '3)', '4)', '5)', '6)', '7)', '8)', '9)', '10)',
                               '1 -', '2 -', '3 -', '4 -', '5 -', '6 -', '7 -', '8 -', '9 -', '10 -']:
                    if line.startswith(pattern):
                        cleaned = line[len(pattern):].strip()
                        break
                
                if cleaned and len(cleaned) > 3:  # Reasonable length check
                    suggestions.append(cleaned)
        
        return suggestions

    def _generate_fallback_topics(self, business: Business, content_type: str, category: Optional[str]) -> List[str]:
        """Fallback topics if AI fails"""
        industry = business.industry or 'business'
        business_name = business.name
        
        fallback_topics = [
            f"5 Essential {industry} Tips for Beginners",
            f"How {business_name} is Transforming the {industry} Industry",
            f"The Future of {industry}: Trends to Watch",
            f"Common {industry} Mistakes and How to Avoid Them",
            f"Why Choose {business_name} for Your {industry} Needs"
        ]
        
        return fallback_topics

    def _generate_fallback_keywords(self, business: Business, content_type: str, category: Optional[str]) -> List[str]:
        """Fallback keywords if AI fails"""
        industry = business.industry or 'business'
        business_name = business.name.lower()
        
        fallback_keywords = [
            industry.lower(),
            business_name,
            f"{industry.lower()} services",
            f"{industry.lower()} tips",
            "professional",
            f"{industry.lower()} solutions",
            f"best {industry.lower()}",
            f"{industry.lower()} expert",
            f"{industry.lower()} guide",
            f"{business_name} {industry.lower()}"
        ]
        
        return fallback_keywords[:10]