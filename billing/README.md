

# Billing System Module

This module implements a comprehensive billing system for the multi-agent platform with token-based pricing and team management features.

## Features

- **Token-based billing**: Charge based on input, LLM, and output tokens
- **Team management**: Support for team-based pricing with member limits
- **Modular tariffs**: Flexible tariff plans with configurable components
- **Admin API**: Endpoints for managing tariffs and components
- **Pipeline integration**: Easy integration with information processing pipelines

## Components

### Models

- `TariffPlan`: Represents a pricing plan with components
- `OrganizationBalance`: Tracks organization balance and team members
- `TariffComponent`: Individual billable components (agents, features, etc.)

### Managers

- `TokenBasedBillingManager`: Handles token-based charging
- `TeamBillingManager`: Manages team member additions and billing
- `InputTokenMonitor`, `OutputTokenMonitor`, `LLMTokenMonitor`: Token usage tracking

### Integration

- `BilledInformationPipeline`: Example pipeline with billing integration

## Setup

1. Install requirements:
   ```bash
   pip install -r billing/requirements.txt
   ```

2. Set up database:
   ```python
   from billing.models import Base, engine
   Base.metadata.create_all(engine)
   ```

## Usage

### Basic Pipeline Integration

```python
from sqlalchemy.orm import sessionmaker
from billing.models import Base, engine
from billing.pipeline_integration import BilledInformationPipeline

# Set up database
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Create pipeline
pipeline = BilledInformationPipeline(session, "org-id", "user-id")

# Process data
result = pipeline.process("Sample input data")
print(result)
```

### Admin API

Run the admin API:
```bash
python billing/admin_api.py
```

Create a tariff via API:
```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "name": "Basic Plan",
    "price_per_month": 99.99,
    "max_team_members": 5,
    "member_price": 19.99
}' http://localhost:5001/api/v1/admin/tariffs
```

## Architecture

The billing system follows a modular architecture:

1. **Models**: Database schema for tariffs, balances, and components
2. **Managers**: Business logic for billing operations
3. **Monitors**: Token usage tracking
4. **Integration**: Pipeline and service connectors
5. **Admin**: API and interfaces for configuration

This design allows for flexible pricing models and easy integration with existing systems.

