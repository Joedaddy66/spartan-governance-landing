"""
Database models for Stripe Webhook integration and Marketplace stores
"""
from sqlalchemy import Column, String, Integer, DateTime, JSON, Boolean, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class StripeStore(Base):
    """Marketplace store created from Stripe Connect account"""
    __tablename__ = "stripe_stores"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    stripe_account_id = Column(String, unique=True, nullable=False, index=True)
    store_name = Column(String, nullable=False)
    description = Column(Text)
    email = Column(String, nullable=False)
    phone = Column(String)
    country = Column(String, default="US")
    
    # Store configuration
    store_pages = Column(JSON, default={})
    settings = Column(JSON, default={})
    payment_methods = Column(JSON, default={})
    seller_info = Column(JSON, default={})
    
    # Status tracking
    status = Column(String, default="active")  # active, inactive, suspended
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<StripeStore {self.store_name} ({self.stripe_account_id})>"


class MarketplaceCustomer(Base):
    """Customer data synced from Stripe"""
    __tablename__ = "marketplace_customers"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    stripe_customer_id = Column(String, unique=True, nullable=False, index=True)
    stripe_store_id = Column(String, nullable=False, index=True)
    
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    phone = Column(String)
    
    # Address information
    address = Column(JSON, default={})
    
    # Customer metadata
    metadata = Column(JSON, default={})
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Customer {self.name} ({self.stripe_customer_id})>"


class MarketplaceOrder(Base):
    """Order tracking for marketplace transactions"""
    __tablename__ = "marketplace_orders"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    stripe_charge_id = Column(String, unique=True, nullable=False, index=True)
    stripe_payment_intent_id = Column(String, index=True)
    stripe_store_id = Column(String, nullable=False, index=True)
    customer_id = Column(String, nullable=False, index=True)
    
    # Order information
    amount = Column(Float, nullable=False)
    currency = Column(String, default="usd")
    status = Column(String, default="pending")  # pending, completed, failed, refunded
    
    # Product/Service details
    items = Column(JSON, default=[])
    description = Column(Text)
    metadata = Column(JSON, default={})
    
    # Payment details
    payment_method = Column(String, default="stripe")
    receipt_url = Column(String)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Order {self.id} - {self.status}>"


class StripeWebhookEvent(Base):
    """Log of all Stripe webhook events for audit trail"""
    __tablename__ = "stripe_webhook_events"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    stripe_event_id = Column(String, unique=True, nullable=False, index=True)
    event_type = Column(String, nullable=False, index=True)
    
    # Event data
    event_data = Column(JSON, nullable=False)
    status = Column(String, default="processed")  # processed, failed, pending
    
    # Processing information
    processed_at = Column(DateTime, default=datetime.utcnow)
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<WebhookEvent {self.event_type} - {self.status}>"


class MarketplaceProduct(Base):
    """Products available in marketplace store"""
    __tablename__ = "marketplace_products"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    stripe_store_id = Column(String, nullable=False, index=True)
    stripe_product_id = Column(String, index=True)
    
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    currency = Column(String, default="usd")
    
    # Product details
    category = Column(String)
    image_url = Column(String)
    inventory = Column(Integer, default=0)
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Metadata
    metadata = Column(JSON, default={})
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<Product {self.name}>"
