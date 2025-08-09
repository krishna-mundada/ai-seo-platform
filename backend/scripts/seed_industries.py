#!/usr/bin/env python3
"""
Seed script to populate initial industry data.
Run from backend directory: python scripts/seed_industries.py
"""
import sys
import os

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.industry import Industry

# Initial industry data with modern categories
INITIAL_INDUSTRIES = [
    {
        "name": "Technology",
        "slug": "technology",
        "description": "Software, hardware, IT services, and tech startups",
        "icon": "💻",
        "color": "#3B82F6",  # Blue
        "sort_order": 1
    },
    {
        "name": "Marketing & Advertising",
        "slug": "marketing-advertising",
        "description": "Digital marketing, advertising agencies, and promotional services",
        "icon": "📢",
        "color": "#F59E0B",  # Amber
        "sort_order": 2
    },
    {
        "name": "Healthcare",
        "slug": "healthcare",
        "description": "Medical services, pharmaceuticals, and health technology",
        "icon": "🏥",
        "color": "#EF4444",  # Red
        "sort_order": 3
    },
    {
        "name": "Finance & Banking",
        "slug": "finance-banking",
        "description": "Financial services, banking, insurance, and fintech",
        "icon": "💰",
        "color": "#10B981",  # Green
        "sort_order": 4
    },
    {
        "name": "Education",
        "slug": "education",
        "description": "Educational institutions, online learning, and training services",
        "icon": "🎓",
        "color": "#8B5CF6",  # Purple
        "sort_order": 5
    },
    {
        "name": "E-commerce & Retail",
        "slug": "ecommerce-retail",
        "description": "Online stores, retail businesses, and marketplace platforms",
        "icon": "🛍️",
        "color": "#EC4899",  # Pink
        "sort_order": 6
    },
    {
        "name": "Manufacturing",
        "slug": "manufacturing",
        "description": "Production, industrial services, and manufacturing companies",
        "icon": "🏭",
        "color": "#6B7280",  # Gray
        "sort_order": 7
    },
    {
        "name": "Consulting",
        "slug": "consulting",
        "description": "Business consulting, professional services, and advisory",
        "icon": "💼",
        "color": "#1F2937",  # Dark Gray
        "sort_order": 8
    },
    {
        "name": "Real Estate",
        "slug": "real-estate",
        "description": "Property management, real estate agencies, and construction",
        "icon": "🏠",
        "color": "#059669",  # Emerald
        "sort_order": 9
    },
    {
        "name": "Food & Beverage",
        "slug": "food-beverage",
        "description": "Restaurants, food services, and beverage companies",
        "icon": "🍕",
        "color": "#DC2626",  # Red
        "sort_order": 10
    },
    {
        "name": "Travel & Tourism",
        "slug": "travel-tourism",
        "description": "Travel agencies, hotels, and tourism services",
        "icon": "✈️",
        "color": "#0284C7",  # Sky Blue
        "sort_order": 11
    },
    {
        "name": "Entertainment & Media",
        "slug": "entertainment-media",
        "description": "Media companies, entertainment, and content creation",
        "icon": "🎬",
        "color": "#7C3AED",  # Violet
        "sort_order": 12
    },
    {
        "name": "Non-Profit",
        "slug": "non-profit",
        "description": "Non-profit organizations and charitable institutions",
        "icon": "❤️",
        "color": "#BE185D",  # Rose
        "sort_order": 13
    },
    {
        "name": "Legal Services",
        "slug": "legal-services",
        "description": "Law firms, legal consultancy, and compliance services",
        "icon": "⚖️",
        "color": "#374151",  # Gray
        "sort_order": 14
    },
    {
        "name": "Automotive",
        "slug": "automotive",
        "description": "Car dealerships, automotive services, and transportation",
        "icon": "🚗",
        "color": "#1E40AF",  # Blue
        "sort_order": 15
    },
    {
        "name": "Other",
        "slug": "other",
        "description": "Industries not covered by other categories",
        "icon": "🔧",
        "color": "#6B7280",  # Gray
        "sort_order": 99
    }
]

def seed_industries():
    """Seed initial industry data"""
    db = SessionLocal()
    try:
        print("🌱 Seeding industries...")
        
        # Check if industries already exist
        existing_count = db.query(Industry).count()
        if existing_count > 0:
            print(f"⚠️  Found {existing_count} existing industries. Skipping seed.")
            print("   Use --force to override existing data.")
            return
        
        # Create industries
        created_count = 0
        for industry_data in INITIAL_INDUSTRIES:
            # Check if this specific industry already exists
            existing = db.query(Industry).filter(Industry.slug == industry_data["slug"]).first()
            if not existing:
                industry = Industry(**industry_data)
                db.add(industry)
                created_count += 1
                print(f"   ✅ Created: {industry_data['name']}")
            else:
                print(f"   ⏭️  Skipped: {industry_data['name']} (already exists)")
        
        db.commit()
        print(f"\n🎉 Successfully seeded {created_count} industries!")
        
        # Display summary
        total_industries = db.query(Industry).count()
        active_industries = db.query(Industry).filter(Industry.is_active == True).count()
        print(f"📊 Database now contains {total_industries} industries ({active_industries} active)")
        
    except Exception as e:
        print(f"❌ Error seeding industries: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

def force_seed_industries():
    """Force seed - updates existing industries"""
    db = SessionLocal()
    try:
        print("🌱 Force seeding industries...")
        
        updated_count = 0
        created_count = 0
        
        for industry_data in INITIAL_INDUSTRIES:
            existing = db.query(Industry).filter(Industry.slug == industry_data["slug"]).first()
            if existing:
                # Update existing
                for key, value in industry_data.items():
                    setattr(existing, key, value)
                updated_count += 1
                print(f"   🔄 Updated: {industry_data['name']}")
            else:
                # Create new
                industry = Industry(**industry_data)
                db.add(industry)
                created_count += 1
                print(f"   ✅ Created: {industry_data['name']}")
        
        db.commit()
        print(f"\n🎉 Successfully processed industries!")
        print(f"   Created: {created_count}")
        print(f"   Updated: {updated_count}")
        
    except Exception as e:
        print(f"❌ Error force seeding industries: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Seed initial industry data")
    parser.add_argument("--force", action="store_true", help="Force update existing industries")
    args = parser.parse_args()
    
    if args.force:
        force_seed_industries()
    else:
        seed_industries()