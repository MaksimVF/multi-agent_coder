


import uuid
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import TariffPlan, OrganizationBalance, TariffComponent, Base

class BillingException(Exception):
    pass

class TokenBasedBillingManager:
    @staticmethod
    def charge_tokens(session, organization_id, input_tokens, llm_tokens, output_tokens, user_id):
        """
        Charge tokens based on usage
        """
        # Calculate total tokens
        total_tokens = input_tokens + llm_tokens + output_tokens

        # Get organization balance
        org_balance = session.query(OrganizationBalance).filter_by(organization_id=organization_id).first()
        if not org_balance:
            raise BillingException("Organization not found")

        # Calculate cost (simplified - in real implementation this would use component pricing)
        token_price = 0.001  # Example: $0.001 per token
        total_cost = total_tokens * token_price

        # Check balance
        if org_balance.balance < total_cost:
            raise BillingException("Insufficient balance")

        # Deduct from balance
        org_balance.balance -= total_cost
        session.commit()

        return {
            'organization_id': organization_id,
            'user_id': user_id,
            'input_tokens': input_tokens,
            'llm_tokens': llm_tokens,
            'output_tokens': output_tokens,
            'total_tokens': total_tokens,
            'total_cost': total_cost,
            'remaining_balance': org_balance.balance
        }

class TeamBillingManager:
    @staticmethod
    def add_team_member(session, organization_id):
        """
        Add a team member to an organization
        """
        # Get organization balance
        org_balance = session.query(OrganizationBalance).filter_by(organization_id=organization_id).first()
        if not org_balance:
            raise BillingException("Organization not found")

        # Get tariff plan
        tariff = session.query(TariffPlan).get(org_balance.tariff_plan_id)
        if not tariff:
            raise BillingException("Tariff plan not found")

        # Check team member limit
        if org_balance.team_members >= tariff.max_team_members:
            raise BillingException("Team member limit reached")

        # Calculate cost
        cost = tariff.member_price

        # Check balance
        if org_balance.balance < cost:
            raise BillingException("Insufficient balance for adding team member")

        # Deduct cost and add member
        org_balance.balance -= cost
        org_balance.team_members += 1
        session.commit()

        return {
            'organization_id': organization_id,
            'new_team_members': org_balance.team_members,
            'cost': cost,
            'remaining_balance': org_balance.balance
        }

class InputTokenMonitor:
    def __init__(self, session, organization_id, user_id):
        self.session = session
        self.organization_id = organization_id
        self.user_id = user_id

    def monitor(self, tokens):
        """
        Monitor input tokens and charge for them
        """
        return TokenBasedBillingManager.charge_tokens(
            self.session,
            self.organization_id,
            input_tokens=tokens,
            llm_tokens=0,
            output_tokens=0,
            user_id=self.user_id
        )

class LLMTokenMonitor:
    def __init__(self, session, organization_id, user_id):
        self.session = session
        self.organization_id = organization_id
        self.user_id = user_id

    def monitor(self, tokens):
        """
        Monitor LLM tokens and charge for them
        """
        return TokenBasedBillingManager.charge_tokens(
            self.session,
            self.organization_id,
            input_tokens=0,
            llm_tokens=tokens,
            output_tokens=0,
            user_id=self.user_id
        )

class OutputTokenMonitor:
    def __init__(self, session, organization_id, user_id):
        self.session = session
        self.organization_id = organization_id
        self.user_id = user_id

    def monitor(self, tokens):
        """
        Monitor output tokens and charge for them
        """
        return TokenBasedBillingManager.charge_tokens(
            self.session,
            self.organization_id,
            input_tokens=0,
            llm_tokens=0,
            output_tokens=tokens,
            user_id=self.user_id
        )

