"""Fixed registry of the Avina signals for the CA/TX/FL retirement-lead
campaign in the "Dailysolutions" workspace. Mirrors docs/avina-signal-campaign.md
-- update both places together if a signal is recreated or renamed.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Segment:
    campaign_segment: str
    signal_id: str
    state: str  # two-letter code
    target_profession_group: str  # education | nursing | physician | fire_service | public_employee | business_owner


# The 18 state x profession-group signals, in rotation order. One is
# generated per scheduled run (see __init__.py) until all 18 have at least
# one batch, then the rotation reports complete and stops spending credits.
SEGMENTS: list[Segment] = [
    Segment("ca-education-signals", "e246145f-f130-4408-a2d8-3b4b908f5892", "CA", "education"),
    Segment("ca-healthcare-signals", "0c9cf148-640a-40bb-a53c-f4615e277e6a", "CA", "nursing"),
    Segment("ca-physician-signals", "48da55c9-75a8-4d58-896e-15554c88e6b7", "CA", "physician"),
    Segment("ca-fire-service-signals", "234c917c-0979-4e7d-bf42-8f73751d8871", "CA", "fire_service"),
    Segment("ca-public-employee-signals", "5efb1c64-f6e9-4a92-94d3-816a4031470c", "CA", "public_employee"),
    Segment("ca-business-owner-signals", "02f4e747-4330-478d-9871-d512652a624d", "CA", "business_owner"),
    Segment("tx-education-signals", "7973a449-49cc-4057-b98a-816b0505a5af", "TX", "education"),
    Segment("tx-healthcare-signals", "f34d678f-0522-45fb-8d01-83eb719bc34f", "TX", "nursing"),
    Segment("tx-physician-signals", "6824aaf0-52bf-42f1-a236-c53ad598c805", "TX", "physician"),
    Segment("tx-fire-service-signals", "12999e1f-afe0-4bf2-a7c2-12d7682936ff", "TX", "fire_service"),
    Segment("tx-public-employee-signals", "3237082f-ec95-4821-a734-37987bed5b2a", "TX", "public_employee"),
    Segment("tx-business-owner-signals", "c53bbd6b-8b71-4639-92d8-8e27edf74240", "TX", "business_owner"),
    Segment("fl-education-signals", "18561e17-96da-415a-a1b2-c61e1fd0b099", "FL", "education"),
    Segment("fl-healthcare-signals", "eb8600af-6f18-4005-96c5-976e65a00da0", "FL", "nursing"),
    Segment("fl-physician-signals", "b4f52b4a-8a2f-4beb-88db-38b0d1c7c39d", "FL", "physician"),
    Segment("fl-fire-service-signals", "c96cdb42-8fd5-46c5-8dfe-bf3537df926b", "FL", "fire_service"),
    Segment("fl-public-employee-signals", "62afe135-cc06-492e-b95f-92cd4b084628", "FL", "public_employee"),
    Segment("fl-business-owner-signals", "2cea8478-39ac-4023-bafc-333139f787d6", "FL", "business_owner"),
]

# The original cross-segment signal, kept for reference only. Not part of the
# rotation (superseded by the 18 segments; see docs/avina-signal-campaign.md).
COMBINED_SIGNAL_ID = "a5f91c4d-bc31-4aeb-9207-f9582c3664e6"

WORKSPACE = "Dailysolutions"
LEADS_PER_RUN = 10
