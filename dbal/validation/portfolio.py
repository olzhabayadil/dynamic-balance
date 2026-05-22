from pydantic import BaseModel, ConfigDict

from dbal.products import Deal


class PortfolioValidationIssue(BaseModel):
    model_config = ConfigDict(frozen=True)

    deal_id: str
    field: str
    message: str


def validate_deals(deals: list[Deal]) -> list[PortfolioValidationIssue]:
    seen: set[str] = set()
    issues: list[PortfolioValidationIssue] = []
    for deal in deals:
        if deal.deal_id in seen:
            issues.append(
                PortfolioValidationIssue(
                    deal_id=deal.deal_id,
                    field="deal_id",
                    message="duplicate deal_id",
                )
            )
        seen.add(deal.deal_id)
    return issues
