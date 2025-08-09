import {
  Stack,
  Text,
  Card,
  Select,
  TextInput,
  Textarea,
  TagsInput,
  Button,
  Group,
  Grid,
  Badge,
  LoadingOverlay,
  Alert
} from '@mantine/core'
import { useForm } from '@mantine/form'
import { useState } from 'react'
import { IconSparkles, IconInfoCircle, IconCheck, IconEdit, IconThumbUp, IconSend, IconDeviceFloppy } from '@tabler/icons-react'
import { notifications } from '@mantine/notifications'
import { useQuery } from '@tanstack/react-query'
import { businessApi, contentApi, suggestionsApi } from '../lib/api'
import { useDisclosure } from '@mantine/hooks'
import { EditContentModal } from '../components/EditContentModal'

const contentTypes = [
  { value: 'blog_post', label: 'Blog Post' },
  { value: 'linkedin_post', label: 'LinkedIn Post' },
  { value: 'twitter_post', label: 'Twitter Post' },
  { value: 'facebook_post', label: 'Facebook Post' },
  { value: 'instagram_post', label: 'Instagram Post' },
  { value: 'email', label: 'Email Newsletter' },
]

const postCategories = [
  { value: 'educational', label: '📚 Educational' },
  { value: 'promotional', label: '🚀 Promotional' },
  { value: 'news', label: '📰 Latest News' },
  { value: 'behind_scenes', label: '🎬 Behind the Scenes' },
  { value: 'customer_story', label: '💬 Customer Story' },
  { value: 'how_to', label: '🛠️ How-to Guide' },
  { value: 'industry_insights', label: '💡 Industry Insights' },
  { value: 'company_updates', label: '📢 Company Updates' },
  { value: 'thought_leadership', label: '🎯 Thought Leadership' },
  { value: 'seasonal', label: '🎄 Seasonal Content' },
]

interface Business {
  id: number
  name: string
  industry?: string
  description?: string
  website_url?: string
  target_audience?: string
  brand_voice?: string
  created_at: string
}

interface GeneratedContent {
  id: number
  title: string
  content_text: string
  content_type: string
  meta_description: string
  keywords: string[]
  seo_score: number
  ai_model_used: string
}

export function ContentGenerator() {
  const [loading, setLoading] = useState(false)
  const [generatedContent, setGeneratedContent] = useState<GeneratedContent | null>(null)
  const [editOpened, { open: openEdit, close: closeEdit }] = useDisclosure(false)
  const [approving, setApproving] = useState(false)
  const [publishing, setPublishing] = useState(false)
  const [savingDraft, setSavingDraft] = useState(false)
  const [topicSuggestions, setTopicSuggestions] = useState<string[]>([])
  const [keywordSuggestions, setKeywordSuggestions] = useState<string[]>([])
  const [loadingSuggestions, setLoadingSuggestions] = useState(false)
  const [loadingKeywords, setLoadingKeywords] = useState(false)

  // Fetch businesses
  const { data: businesses = [], isLoading: businessesLoading } = useQuery({
    queryKey: ['businesses'],
    queryFn: () => businessApi.list().then(res => res.data),
  })

  const form = useForm({
    initialValues: {
      business_id: '',
      content_type: '',
      category: '',
      topic: '',
      description: '',
      keywords: [] as string[],
    },
    validate: {
      business_id: (value) => (!value ? 'Please select a business' : null),
      content_type: (value) => (!value ? 'Please select content type' : null),
      topic: (value) => (!value ? 'Please enter a topic' : null),
    },
  })

  const handleSubmit = async (values: typeof form.values) => {
    setLoading(true)
    try {
      // Convert business_id to number and prepare request data
      const requestData = {
        business_id: parseInt(values.business_id),
        content_type: values.content_type,
        topic: values.topic,
        keywords: values.keywords,
        // Include new fields in the request
        category: values.category,
        description: values.description,
      }
      
      console.log('Sending request:', requestData) // Debug log
      
      const response = await fetch('http://localhost:8000/api/v1/content/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      })

      if (!response.ok) {
        throw new Error('Failed to generate content')
      }

      const data = await response.json()
      setGeneratedContent(data)
      
      notifications.show({
        title: 'Content Generated!',
        message: 'Your AI-powered content is ready for review',
        color: 'green',
        icon: <IconCheck size={16} />,
      })
    } catch (error) {
      notifications.show({
        title: 'Generation Failed',
        message: 'There was an error generating content. Please try again.',
        color: 'red',
      })
    } finally {
      setLoading(false)
    }
  }

  const handleEditContent = () => {
    console.log('Edit button clicked', generatedContent)
    if (generatedContent) {
      openEdit()
      console.log('Modal should be open now')
    }
  }

  const handleSaveEdit = (title: string, content: string) => {
    if (generatedContent) {
      setGeneratedContent({
        ...generatedContent,
        title,
        content_text: content
      })
      notifications.show({
        title: 'Content Updated!',
        message: 'Your content has been successfully edited',
        color: 'green',
        icon: <IconCheck size={16} />,
      })
    }
  }

  const handleRegenerate = async () => {
    if (!generatedContent) return
    
    setLoading(true)
    try {
      const requestData = {
        business_id: parseInt(form.values.business_id),
        content_type: form.values.content_type,
        topic: form.values.topic,
        keywords: form.values.keywords,
        category: form.values.category,
        description: form.values.description,
      }
      
      const response = await fetch('http://localhost:8000/api/v1/content/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData),
      })

      if (!response.ok) {
        throw new Error('Failed to regenerate content')
      }

      const data = await response.json()
      setGeneratedContent(data)
      
      notifications.show({
        title: 'Content Regenerated!',
        message: 'New AI-powered content has been generated',
        color: 'blue',
        icon: <IconSparkles size={16} />,
      })
    } catch (error) {
      notifications.show({
        title: 'Regeneration Failed',
        message: 'There was an error regenerating content. Please try again.',
        color: 'red',
      })
    } finally {
      setLoading(false)
    }
  }

  const handleSaveDraft = async () => {
    if (!generatedContent?.id) return
    
    setSavingDraft(true)
    try {
      await contentApi.saveDraft(generatedContent.id)
      
      notifications.show({
        title: 'Draft Saved!',
        message: 'Content has been saved as draft to database',
        color: 'blue',
        icon: <IconDeviceFloppy size={16} />,
      })
    } catch (error) {
      notifications.show({
        title: 'Save Failed',
        message: 'There was an error saving the draft. Please try again.',
        color: 'red',
      })
    } finally {
      setSavingDraft(false)
    }
  }

  const handleApprove = async () => {
    if (!generatedContent?.id) return
    
    setApproving(true)
    try {
      await contentApi.approve(generatedContent.id)
      
      notifications.show({
        title: 'Content Approved!',
        message: 'Content has been approved and saved to database',
        color: 'green',
        icon: <IconThumbUp size={16} />,
      })
    } catch (error) {
      notifications.show({
        title: 'Approval Failed',
        message: 'There was an error approving the content. Please try again.',
        color: 'red',
      })
    } finally {
      setApproving(false)
    }
  }

  const handlePublish = async () => {
    if (!generatedContent) return
    
    setPublishing(true)
    try {
      // Simulate delay for publishing process
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Show not implemented message for now
      notifications.show({
        title: 'Publishing Not Available',
        message: 'Publishing functionality will be implemented in a future update',
        color: 'orange',
        icon: <IconSend size={16} />,
      })
    } finally {
      setPublishing(false)
    }
  }

  const generateTopicSuggestions = async () => {
    if (!form.values.business_id || !form.values.content_type) {
      return
    }

    setLoadingSuggestions(true)
    try {
      const response = await suggestionsApi.topics({
        business_id: parseInt(form.values.business_id),
        content_type: form.values.content_type,
        category: form.values.category || undefined,
        description: form.values.description || undefined,
      })
      
      setTopicSuggestions(response.data.suggestions)
      
    } catch (error) {
      console.error('Failed to generate AI topic suggestions:', error)
      notifications.show({
        title: 'Suggestions Failed',
        message: 'Could not generate topic suggestions. Please try again.',
        color: 'red',
      })
      
      // Fallback to hardcoded suggestions if AI fails
      const business = businesses.find((b: { id: { toString: () => string } }) => b.id.toString() === form.values.business_id)
      if (business) {
        const fallbackSuggestions = getTopicSuggestions(business, form.values.content_type, form.values.category)
        setTopicSuggestions(fallbackSuggestions)
      }
    } finally {
      setLoadingSuggestions(false)
    }
  }

  const getTopicSuggestions = (business: Business, contentType: string, category?: string): string[] => {
    const businessName = business.name
    const industry = business.industry || 'business'
    
    // All possible suggestions organized by category and content type
    const suggestionMap: Record<string, Record<string, string[]>> = {
      educational: {
        blog_post: [
          `5 Essential ${industry} Trends Every Professional Should Know`,
          `The Complete Guide to Getting Started in ${industry}`,
          `Common ${industry} Mistakes and How to Avoid Them`,
          `What is ${industry}? A Beginner's Guide`,
          `Top 10 Best Practices for ${industry} Success`
        ],
        linkedin_post: [
          `3 key lessons I learned in ${industry}`,
          `Why ${industry} professionals need to focus on continuous learning`,
          `The biggest misconception about ${industry}`,
          `Skills every ${industry} professional should develop`,
          `How ${industry} has changed in the past 5 years`
        ],
        twitter_post: [
          `Quick tip for ${industry} beginners:`,
          `The #1 mistake in ${industry} is...`,
          `${industry} fact of the day:`,
          `Pro tip: In ${industry}, always remember to...`,
          `Thread: Essential ${industry} skills 🧵`
        ]
      },
      promotional: {
        blog_post: [
          `Why ${businessName} is the Perfect Solution for Your ${industry} Needs`,
          `How ${businessName} Helps ${industry} Professionals Save Time and Money`,
          `Case Study: How We Helped a ${industry} Company Grow 300%`,
          `What Makes ${businessName} Different in the ${industry} Space`,
          `The ${businessName} Advantage: Features That Matter`
        ],
        linkedin_post: [
          `Excited to announce our latest ${industry} solution at ${businessName}`,
          `Here's how ${businessName} is transforming ${industry}`,
          `Client spotlight: Amazing results in ${industry}`,
          `Why we built ${businessName} for ${industry} professionals`,
          `The future of ${industry} with ${businessName}`
        ],
        twitter_post: [
          `🚀 New feature alert at ${businessName}!`,
          `${businessName} is now available for ${industry}`,
          `Join thousands of ${industry} professionals using ${businessName}`,
          `Special offer for ${industry} professionals`,
          `${businessName} + ${industry} = Perfect match ✨`
        ]
      },
      news: {
        blog_post: [
          `Breaking: Major Changes Coming to ${industry} in 2024`,
          `${industry} Industry Report: Key Takeaways and Trends`,
          `How Recent ${industry} Developments Affect Your Business`,
          `Market Update: What's Happening in ${industry} Right Now`,
          `Regulatory Changes in ${industry}: What You Need to Know`
        ],
        linkedin_post: [
          `Big news in the ${industry} world today`,
          `Industry update: ${industry} sees major changes`,
          `What this week's ${industry} news means for professionals`,
          `My take on the latest ${industry} developments`,
          `Breaking: ${industry} industry reaches new milestone`
        ]
      },
      how_to: {
        blog_post: [
          `How to Get Started in ${industry}: Step-by-Step Guide`,
          `How to Choose the Right ${industry} Solution for Your Business`,
          `How to Optimize Your ${industry} Strategy in 2024`,
          `How to Avoid Common ${industry} Pitfalls`,
          `How to Scale Your ${industry} Operations Effectively`
        ],
        linkedin_post: [
          `How I streamlined our ${industry} process`,
          `Step-by-step guide to ${industry} success`,
          `How to build a career in ${industry}`,
          `The process that transformed our ${industry} approach`,
          `How we solved our biggest ${industry} challenge`
        ]
      }
    }

    // If no category is selected, mix suggestions from all categories
    let allSuggestions: string[] = []
    
    if (category && suggestionMap[category]) {
      const categoryMap = suggestionMap[category]
      allSuggestions = categoryMap[contentType] || categoryMap.blog_post || []
    } else {
      // Mix suggestions from all categories if no category selected
      Object.values(suggestionMap).forEach(categoryMap => {
        const suggestions = categoryMap[contentType] || categoryMap.blog_post || []
        allSuggestions.push(...suggestions)
      })
    }
    
    // Shuffle array and return 5 random suggestions each time
    const shuffled = [...allSuggestions].sort(() => Math.random() - 0.5)
    return shuffled.slice(0, 5)
  }

  const generateKeywordSuggestions = async () => {
    if (!form.values.business_id || !form.values.content_type) {
      return
    }

    setLoadingKeywords(true)
    try {
      const response = await suggestionsApi.keywords({
        business_id: parseInt(form.values.business_id),
        content_type: form.values.content_type,
        category: form.values.category || undefined,
        topic: form.values.topic || undefined,
        description: form.values.description || undefined,
      })
      
      setKeywordSuggestions(response.data.suggestions)
      
    } catch (error) {
      console.error('Failed to generate AI keyword suggestions:', error)
      notifications.show({
        title: 'Keywords Failed',
        message: 'Could not generate keyword suggestions. Please try again.',
        color: 'red',
      })
      
      // Fallback to hardcoded suggestions if AI fails
      const business = businesses.find((b: { id: { toString: () => string } }) => b.id.toString() === form.values.business_id)
      if (business) {
        const fallbackSuggestions = getKeywordSuggestions(business, form.values.content_type, form.values.category, form.values.topic)
        setKeywordSuggestions(fallbackSuggestions)
      }
    } finally {
      setLoadingKeywords(false)
    }
  }

  const getKeywordSuggestions = (business: Business, contentType: string, category?: string, topic?: string): string[] => {
    const businessName = business.name
    const industry = business.industry || 'business'
    
    // Base keywords for different industries and content types
    const industryKeywords: Record<string, string[]> = {
      'Technology': ['tech', 'digital', 'innovation', 'software', 'AI', 'automation', 'cloud', 'cybersecurity', 'data'],
      'Healthcare': ['health', 'medical', 'wellness', 'patient care', 'treatment', 'diagnosis', 'prevention', 'medicine'],
      'Finance & Banking': ['finance', 'banking', 'investment', 'money', 'financial planning', 'loans', 'savings', 'credit'],
      'Education': ['education', 'learning', 'teaching', 'students', 'curriculum', 'skills', 'training', 'development'],
      'Marketing & Advertising': ['marketing', 'advertising', 'branding', 'digital marketing', 'SEO', 'social media', 'campaigns'],
      'E-commerce & Retail': ['ecommerce', 'retail', 'shopping', 'products', 'customers', 'sales', 'online store'],
      'Manufacturing': ['manufacturing', 'production', 'quality', 'efficiency', 'supply chain', 'industrial', 'process'],
      'Real Estate': ['real estate', 'property', 'housing', 'investment', 'market', 'buying', 'selling', 'rental'],
      'Food & Beverage': ['food', 'restaurant', 'cuisine', 'dining', 'nutrition', 'recipes', 'culinary', 'beverage'],
      'Travel & Tourism': ['travel', 'tourism', 'vacation', 'destinations', 'hotels', 'flights', 'adventure', 'experience']
    }

    // Content type specific keywords
    const contentTypeKeywords: Record<string, string[]> = {
      'blog_post': ['SEO', 'content marketing', 'blog', 'article', 'guide', 'tips', 'how-to', 'best practices'],
      'linkedin_post': ['professional', 'networking', 'career', 'business', 'LinkedIn', 'industry insights', 'leadership'],
      'twitter_post': ['trending', 'hashtags', 'Twitter', 'viral', 'engagement', 'social media', 'quick tips'],
      'facebook_post': ['Facebook', 'community', 'engagement', 'social', 'sharing', 'discussion', 'audience'],
      'instagram_post': ['Instagram', 'visual', 'photos', 'stories', 'aesthetic', 'lifestyle', 'inspiration'],
      'email': ['email marketing', 'newsletter', 'subscribers', 'campaigns', 'personalization', 'conversion']
    }

    // Category specific keywords
    const categoryKeywords: Record<string, string[]> = {
      'educational': ['tutorial', 'guide', 'learning', 'education', 'training', 'skills', 'knowledge', 'tips'],
      'promotional': ['sale', 'offer', 'discount', 'promotion', 'deal', 'limited time', 'exclusive', 'special'],
      'news': ['news', 'update', 'announcement', 'breaking', 'latest', 'current', 'trending', 'industry news'],
      'behind_scenes': ['behind the scenes', 'team', 'culture', 'process', 'story', 'journey', 'insider'],
      'customer_story': ['customer', 'testimonial', 'success story', 'case study', 'client', 'results', 'experience'],
      'how_to': ['how to', 'step by step', 'tutorial', 'guide', 'instructions', 'DIY', 'beginner'],
      'industry_insights': ['insights', 'analysis', 'trends', 'market', 'industry', 'expert opinion', 'forecast'],
      'company_updates': ['company news', 'updates', 'announcements', 'milestones', 'achievements', 'growth'],
      'thought_leadership': ['thought leadership', 'expert', 'opinion', 'vision', 'innovation', 'future', 'strategy'],
      'seasonal': ['seasonal', 'holiday', 'special occasion', 'celebration', 'festive', 'limited time']
    }

    // Collect all relevant keywords
    let allKeywords: string[] = []
    
    // Add industry keywords
    const industryKeys = Object.keys(industryKeywords).find(key => 
      industry.toLowerCase().includes(key.toLowerCase()) || key.toLowerCase().includes(industry.toLowerCase())
    )
    if (industryKeys) {
      allKeywords.push(...industryKeywords[industryKeys])
    } else {
      allKeywords.push(industry.toLowerCase(), 'business', 'professional', 'services')
    }
    
    // Add content type keywords
    if (contentTypeKeywords[contentType]) {
      allKeywords.push(...contentTypeKeywords[contentType])
    }
    
    // Add category keywords
    if (category && categoryKeywords[category]) {
      allKeywords.push(...categoryKeywords[category])
    }
    
    // Add business name variations
    allKeywords.push(businessName.toLowerCase())
    if (businessName.includes(' ')) {
      allKeywords.push(...businessName.toLowerCase().split(' '))
    }
    
    // Add topic-based keywords if topic exists
    if (topic) {
      const topicWords = topic.toLowerCase()
        .replace(/[^\w\s]/g, ' ')
        .split(' ')
        .filter(word => word.length > 2)
        .slice(0, 3) // Take first 3 meaningful words from topic
      allKeywords.push(...topicWords)
    }
    
    // Remove duplicates and shuffle
    const uniqueKeywords = Array.from(new Set(allKeywords))
    const shuffled = uniqueKeywords.sort(() => Math.random() - 0.5)
    
    // Return 8-10 keyword suggestions
    return shuffled.slice(0, 10)
  }

  const getContentTypeInfo = (type: string) => {
    const info = {
      blog_post: 'Long-form content (1000-1500 words) optimized for SEO',
      linkedin_post: 'Professional content (200-300 words) for LinkedIn audience',
      twitter_post: 'Short, engaging content under 280 characters with hashtags',
      facebook_post: 'Conversational content (100-200 words) for Facebook',
      instagram_post: 'Visual-focused caption (150-300 words) with hashtags',
      email: 'Newsletter content (500-1000 words) for email campaigns',
    }
    return info[type as keyof typeof info] || ''
  }

  return (
    <Grid>
      <Grid.Col span={{ base: 12, md: 6 }}>
        <Card shadow="sm" padding="lg" radius="md" withBorder>
          <Stack gap="md">
            <Group>
              <IconSparkles size={24} color="blue" />
              <Text size="xl" fw={700}>
                AI Content Generator
              </Text>
            </Group>

            <form onSubmit={form.onSubmit(handleSubmit)}>
              <Stack gap="md">
                <Select
                  label="Business"
                  placeholder={businessesLoading ? "Loading businesses..." : "Select a business"}
                  data={businesses.map((business: Business) => ({
                    value: business.id.toString(),
                    label: business.name
                  }))}
                  disabled={businessesLoading}
                  {...form.getInputProps('business_id')}
                  required
                />

                <Select
                  label="Content Type"
                  placeholder="Choose content type"
                  data={contentTypes}
                  {...form.getInputProps('content_type')}
                  onChange={(value) => {
                    form.setFieldValue('content_type', value || '')
                    setTopicSuggestions([]) // Clear suggestions when type changes
                  }}
                  required
                />

                <Select
                  label="Content Category"
                  placeholder="Choose content category (optional)"
                  data={postCategories}
                  {...form.getInputProps('category')}
                  onChange={(value) => {
                    form.setFieldValue('category', value || '')
                    setTopicSuggestions([]) // Clear suggestions when category changes
                  }}
                  description="Optional: Select a category to get topic suggestions"
                />

                {form.values.content_type && (
                  <Alert icon={<IconInfoCircle size={16} />} color="blue" variant="light">
                    {getContentTypeInfo(form.values.content_type)}
                  </Alert>
                )}

                <TextInput
                  label="Topic"
                  placeholder="Enter your content topic"
                  {...form.getInputProps('topic')}
                  required
                />

                {form.values.business_id && form.values.content_type && (
                  <div>
                    <Group justify="space-between" mb="xs">
                      <Text size="sm" fw={500}>Topic Suggestions</Text>
                      <Button
                        size="xs"
                        variant="light"
                        leftSection={<IconSparkles size={14} />}
                        onClick={generateTopicSuggestions}
                        loading={loadingSuggestions}
                      >
                        {topicSuggestions.length > 0 ? 'Get New Suggestions' : 'Get Suggestions'}
                      </Button>
                    </Group>
                    
                    {topicSuggestions.length > 0 && (
                      <Stack gap="xs" mb="md">
                        {topicSuggestions.map((suggestion, index) => (
                          <Card 
                            key={index}
                            padding="sm"
                            withBorder
                            style={{ cursor: 'pointer' }}
                            onClick={() => form.setFieldValue('topic', suggestion)}
                          >
                            <Text size="sm">{suggestion}</Text>
                          </Card>
                        ))}
                        <Text size="xs" c="dimmed">Click any suggestion to use it as your topic</Text>
                      </Stack>
                    )}
                  </div>
                )}

                <Textarea
                  label="Content Description"
                  placeholder="Briefly describe what this content should cover..."
                  {...form.getInputProps('description')}
                  rows={2}
                  description="Optional: Provide context to help generate better content"
                />

                <TagsInput
                  label="Keywords (Optional)"
                  placeholder="Add relevant keywords"
                  {...form.getInputProps('keywords')}
                  description="Press Enter or comma to add keywords"
                />

                {form.values.business_id && form.values.content_type && (
                  <div>
                    <Group justify="space-between" mb="xs">
                      <Text size="sm" fw={500}>Keyword Suggestions</Text>
                      <Button
                        size="xs"
                        variant="light"
                        leftSection={<IconSparkles size={14} />}
                        onClick={generateKeywordSuggestions}
                        loading={loadingKeywords}
                      >
                        {keywordSuggestions.length > 0 ? 'Get New Keywords' : 'Get Keywords'}
                      </Button>
                    </Group>
                    
                    {keywordSuggestions.length > 0 && (
                      <div>
                        <Group gap="xs" mb="sm">
                          {keywordSuggestions.map((keyword, index) => (
                            <Badge
                              key={index}
                              variant="light"
                              style={{ cursor: 'pointer' }}
                              onClick={() => {
                                const currentKeywords = form.values.keywords || []
                                if (!currentKeywords.includes(keyword)) {
                                  form.setFieldValue('keywords', [...currentKeywords, keyword])
                                }
                              }}
                            >
                              {keyword}
                            </Badge>
                          ))}
                        </Group>
                        <Text size="xs" c="dimmed">Click any keyword to add it to your list</Text>
                      </div>
                    )}
                  </div>
                )}

                <Button
                  type="submit"
                  leftSection={<IconSparkles size={16} />}
                  loading={loading}
                  size="md"
                >
                  Generate Content
                </Button>
              </Stack>
            </form>
          </Stack>
        </Card>
      </Grid.Col>

      <Grid.Col span={{ base: 12, md: 6 }}>
        <Card shadow="sm" padding="lg" radius="md" withBorder h="fit-content">
          <LoadingOverlay visible={loading} />
          
          {generatedContent ? (
            <Stack gap="md">
              <Group justify="space-between">
                <Text size="lg" fw={700}>
                  Generated Content
                </Text>
                <Group gap="xs">
                  <Badge color="green" size="sm">
                    SEO: {generatedContent.seo_score}%
                  </Badge>
                  <Badge color="blue" size="sm" variant="light">
                    {generatedContent.ai_model_used}
                  </Badge>
                </Group>
              </Group>

              <div>
                <Text size="sm" fw={600} mb={5}>
                  Title:
                </Text>
                <Text size="sm" c="dimmed">
                  {generatedContent.title}
                </Text>
              </div>

              <div>
                <Text size="sm" fw={600} mb={5}>
                  Content:
                </Text>
                <Card shadow="xs" padding="sm" radius="sm" withBorder>
                  <Text size="sm" style={{ whiteSpace: 'pre-wrap' }}>
                    {generatedContent.content_text}
                  </Text>
                </Card>
              </div>

              {generatedContent.meta_description && (
                <div>
                  <Text size="sm" fw={600} mb={5}>
                    Meta Description:
                  </Text>
                  <Text size="sm" c="dimmed">
                    {generatedContent.meta_description}
                  </Text>
                </div>
              )}

              {generatedContent.keywords.length > 0 && (
                <div>
                  <Text size="sm" fw={600} mb={5}>
                    Keywords:
                  </Text>
                  <Group gap="xs">
                    {generatedContent.keywords.map((keyword, index) => (
                      <Badge key={index} size="sm" variant="light">
                        {keyword}
                      </Badge>
                    ))}
                  </Group>
                </div>
              )}

              <Group gap="sm" mt="md">
                <Button 
                  size="sm" 
                  variant="filled" 
                  color="gray"
                  leftSection={<IconDeviceFloppy size={14} />}
                  onClick={handleSaveDraft}
                  loading={savingDraft}
                >
                  Save Draft
                </Button>
                <Button 
                  size="sm" 
                  variant="filled" 
                  color="green"
                  leftSection={<IconThumbUp size={14} />}
                  onClick={handleApprove}
                  loading={approving}
                >
                  Approve
                </Button>
                <Button 
                  size="sm" 
                  variant="filled" 
                  color="blue"
                  leftSection={<IconSend size={14} />}
                  onClick={handlePublish}
                  loading={publishing}
                >
                  Publish
                </Button>
                <Button 
                  size="sm" 
                  variant="outline"
                  leftSection={<IconEdit size={14} />}
                  onClick={handleEditContent}
                >
                  Edit Content
                </Button>
                <Button 
                  size="sm" 
                  variant="subtle"
                  leftSection={<IconSparkles size={14} />}
                  onClick={handleRegenerate}
                  loading={loading}
                >
                  Regenerate
                </Button>
              </Group>
            </Stack>
          ) : (
            <Stack align="center" gap="md" py="xl">
              <IconSparkles size={48} color="gray" />
              <Text c="dimmed" ta="center">
                Fill out the form to generate AI-powered content
              </Text>
            </Stack>
          )}
        </Card>
      </Grid.Col>

      {/* Edit Content Modal */}
      <EditContentModal
        opened={editOpened}
        onClose={closeEdit}
        title={generatedContent?.title || ''}
        content={generatedContent?.content_text || ''}
        onSave={handleSaveEdit}
      />
    </Grid>
  )
}