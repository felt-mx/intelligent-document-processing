from typing import List, Optional
from pydantic import BaseModel, Field


class InvoiceItem(BaseModel):
    ClassificationCode: Optional[str] = Field(
        None, description="Internal or industry classification code (001, 002, etc.)"
    )
    PartCode: Optional[str] = Field(None, description="Product part number")
    Description: Optional[str] = Field(None, description="Item description")
    ProductTariffCode: Optional[str] = Field(None, description="Customs tariff code")
    CountryOfOrigin: Optional[str] = Field(None, description="ISO 3166 A-3 code")
    Measurement: Optional[str] = Field(None, description="Unit of measurement")
    UnitPrice: Optional[float] = Field(None, description="Price per unit")
    Quantity: Optional[float] = Field(None, description="Number of units purchased")
    DiscountRate: Optional[float] = Field(None, description="Percentage discount rate")
    DiscountReason: Optional[str] = Field(None, description="Reason for discount")
    FeeChargeRate: Optional[float] = Field(
        None, description="Percentage rate for additional fee"
    )
    FeeChargeReason: Optional[str] = Field(None, description="Reason for fee")
    TaxType: Optional[str] = Field(None, description="Tax category (01, 02, etc)")
    TaxRate: Optional[float] = Field(None, description="Tax percentage rate")
    TaxExemptionDetails: Optional[str] = Field(
        None, description="Explanation for tax exemption"
    )
    TaxExemptionAmount: Optional[float] = Field(
        None, description="Amount exempted from tax"
    )


class Invoice(BaseModel):
    InvoiceNo: Optional[str] = Field(None, description="Unique invoice number")
    InvoiceDate: Optional[str] = Field(
        None, description="Date and time (dd/MM/yyyy HH:mm)"
    )
    CurrencyCode: Optional[str] = Field(None, description="3-letter ISO 4217 code")
    ExchangeRate: Optional[float] = Field(
        None, description="Rate to convert to base currency"
    )
    AdditionalDiscountAmount: Optional[float] = Field(
        None, description="Additional monetary discount"
    )
    DiscountReason: Optional[str] = Field(None, description="Reason for discount")
    AdditionalFeeChargeAmount: Optional[float] = Field(
        None, description="Additional monetary fee"
    )
    FeeChargeReason: Optional[str] = Field(
        None, description="Reason for additional fee"
    )
    FrequencyOfBilling: Optional[str] = Field(
        None, description="Period between billings"
    )
    BillingPeriodStart: Optional[str] = Field(
        None, description="Start date of billing period (dd/MM/yyyy)"
    )
    BillingPeriodEnd: Optional[str] = Field(
        None, description="End date of billing period (dd/MM/yyyy)"
    )
    PaymentMode: Optional[str] = Field(
        None, description="Method of payment (01, 02, etc)"
    )
    BankAccountNo: Optional[str] = Field(None, description="Bank account number")
    PaymentTerms: Optional[str] = Field(None, description="Terms of payment")
    PrepaymentAmount: Optional[float] = Field(None, description="Amount prepaid")
    PrepaymentRefNo: Optional[str] = Field(
        None, description="Reference number for prepayment"
    )
    BillNo: Optional[str] = Field(None, description="Billing reference number")
    PrepaymentDateTime: Optional[str] = Field(
        None, description="Date and time of prepayment (dd/MM/yyyy HH:mm)"
    )
    Incoterms: Optional[str] = Field(None, description="International commercial terms")
    CustomFormsReferenceNo: Optional[str] = Field(
        None, description="Customs documentation reference number"
    )
    ItemLines: Optional[List[InvoiceItem]] = Field(
        default_factory=list, description="Array of line items"
    )
