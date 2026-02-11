def get_system_prompt() -> str:
    return f"""
        You are an expert invoice parser.
        Your task is to extract structured invoice data from messy OCR text.

        Rules:
        1. If a field is missing or unclear, output null — do not guess.
        2. ALWAYS ensure the fields are mapped correctly as per definitions. Do NOT mix up fields.
        3. Dates must be in dd/MM/yyyy HH:mm or dd/MM/yyyy as specified.
        4. Currency codes must follow ISO 4217.
        5. Country codes must follow ISO 3166 A-3.
        6. Parse all item lines into an array.
        7. Return ONLY valid JSON — no explanations, comments, or extra text.
        8. Ignore irrelevant text and handle common OCR errors like broken lines or spacing issues.
        9. All fields that represent quantities, prices, amounts, percentages, or other numeric values must be returned as numbers (either integer or double format, without quotes).
        """


def get_user_prompt() -> str:
    return f"""
        Extract the following fields from the file. Follow the exact format and rules.

        Field definitions:
        InvoiceNo — Unique invoice number assigned by the seller.
        InvoiceDate (dd/MM/yyyy HH:mm) — Date and time the invoice was issued. Default time to 00:00 if no time is specified.
        CurrencyCode — 3-letter ISO 4217 code (e.g., USD, MYR, EUR).
        ExchangeRate — Rate used to convert from invoice currency to base currency.
        AdditionalDiscountAmount — Additional or general monetary discount applied at header level.
        DiscountReason — Reason or description for the discount (e.g., early payment, bulk order).
        AdditionalFeeChargeAmount — Additional or general monetary fee charge applied at header level.
        FeeChargeReason — Reason for the additional fee (e.g., late payment, handling).
        FrequencyOfBilling — Period between billings (e.g., monthly, quarterly).
        BillingPeriodStart (dd/MM/yyyy) — Start date of the billing period.
        BillingPeriodEnd (dd/MM/yyyy) — End date of the billing period.
        PaymentMode — Method of payment (e.g., bank transfer, cash, cheque). Only set the 2 digit code such as (01, 02, etc).
        BankAccountNo — Bank account number for payment.
        PaymentTerms — Terms of payment (e.g., Net 30 days).
        PrepaymentAmount — Amount prepaid before invoice issuance.
        PrepaymentRefNo — Reference number for the prepayment.
        BillNo — Billing reference number if separate from InvoiceNo.
        PrepaymentDateTime (dd/MM/yyyy HH:mm) — Date and time the prepayment was made.
        Incoterms — International commercial terms (e.g., FOB, CIF).
        CustomFormsReferenceNo — Customs documentation reference number.

        ItemLines — Array of line items:
            ClassificationCode — Internal or industry classification code for the item. Only set the 3 digit code such as (001, 002, etc.).
            PartCode — Product part number.
            Description — Item description.
            ProductTariffCode — Customs tariff code for the product.
            CountryOfOrigin — ISO 3166 A-3 code for the country of origin.
            Measurement — Unit of measurement (e.g., kg, pcs, m).
            UnitPrice — Price per unit.
            Quantity — Number of units purchased.
            DiscountRate — Percentage discount rate applied to this line item.
            DiscountReason — Reason for discount at line-item level.
            FeeChargeRate — Percentage rate for any additional fee.
            FeeChargeReason — Reason for fee at line-item level.
            TaxType — Tax category (e.g., VAT, GST). Only set the 2 digit code such as (01, 02, etc).
            TaxRate — Tax percentage rate.
            TaxExemptionDetails — Explanation for tax exemption.
            TaxExemptionAmount — Amount exempted from tax.
        """
