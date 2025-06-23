from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

verify_voter_router = APIRouter()

# Address model
class Address(BaseModel):
    division: Optional[str] = None
    district: Optional[str] = None
    upozila: Optional[str] = None
    rmo: Optional[str] = None
    cityCorporationOrMunicipality: Optional[str] = None
    unionOrWard: Optional[str] = None
    postOffice: Optional[str] = None
    postalCode: Optional[str] = None
    wardForUnionPorishod: Optional[int] = None
    additionalMouzaOrMoholla: Optional[str] = None
    additionalVillageOrRoad: Optional[str] = None
    homeOrHoldingNo: Optional[str] = None
    mouzaOrMoholla: Optional[str] = None
    villageOrRoad: Optional[str] = None
    region: Optional[str] = None

# Identify block
class Identify(BaseModel):
    nid10Digit: Optional[str] = None
    nid17Digit: Optional[str] = None
    voterNo: Optional[str] = None
    formNo: Optional[str] = None
    voterId: Optional[str] = None
    dateOfBirth: Optional[str] = None

# Verify block
class Verify(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    nameEn: Optional[str] = None
    gender: Optional[str] = None
    bloodGroup: Optional[str] = None
    dateOfBirth: Optional[str] = None
    father: Optional[str] = None
    mother: Optional[str] = None
    spouse: Optional[str] = None
    nationalId: Optional[str] = None
    pin: Optional[str] = None
    occupation: Optional[str] = None
    permanentAddress: Optional[Address] = None
    presentAddress: Optional[Address] = None
    slno: Optional[int] = None
    formNo: Optional[str] = None
    voterArea: Optional[str] = None
    voterNo: Optional[str] = None
    birthPlace: Optional[str] = None
    disability: Optional[str] = None
    education: Optional[str] = None
    death: Optional[str] = None
    driving: Optional[str] = None
    identification: Optional[str] = None
    marital: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    noFinger: Optional[int] = None
    noFingerprint: Optional[int] = None
    passport: Optional[str] = None
    phone: Optional[str] = None
    religion: Optional[str] = None
    tin: Optional[str] = None
    voterAt: Optional[str] = None
    nidFather: Optional[str] = None
    nidMother: Optional[str] = None
    birthRegistrationNo: Optional[str] = None
    educationOther: Optional[str] = None
    educationSub: Optional[str] = None
    birthOther: Optional[str] = None
    nidSpouse: Optional[str] = None
    deathDateOfFather: Optional[str] = None
    deathDateOfMother: Optional[str] = None
    deathDateOfSpouse: Optional[str] = None
    voterNoFather: Optional[str] = None
    voterNoMother: Optional[str] = None
    voterNoSpouse: Optional[str] = None
    religionOther: Optional[str] = None
    disabilityOther: Optional[str] = None

# Combined request model
class VoterVerifyRequest(BaseModel):
    identify: Identify
    verify: Verify

# API endpoint
@verify_voter_router.post("/verify-voter")
def verify_voter(request: VoterVerifyRequest, authorization: str = Header(None)):
    # Invalid or missing token
    if authorization != "Bearer mocked-access-token":
        return JSONResponse(status_code=403, content={
            "status": "FORBIDDEN",
            "statusCode": "ERROR",
            "error": {"field": "SLA is not Assigned"}
        })

    # Missing identify field
    if not (request.identify.nid10Digit or request.identify.nid17Digit or request.identify.voterNo or request.identify.formNo or request.identify.voterId):
        return JSONResponse(status_code=400, content={
            "status": "BAD_REQUEST",
            "statusCode": "ERROR",
            "error": {
                "field": "nid10Digit/nid17Digit/voterNo/formNo/voterId",
                "message": "Search permission without one of the mandatory fields is not allowed"
            }
        })

    # Empty verify block
    if not request.verify.dict(exclude_unset=True):
        return JSONResponse(status_code=400, content={
            "status": "BAD_REQUEST",
            "statusCode": "ERROR",
            "error": {
                "field": "verify",
                "message": "Please provide voter information for verification"
            }
        })

    # Mismatch simulation
    if request.verify.nameEn != "John Doe":
        return JSONResponse(status_code=406, content={
            "message": "Voter data mismatch",
            "status": "NOT_ACCEPTABLE",
            "verified": False,
            "fieldVerificationResult": {
                "nameEn": False,
                "nationalId": False,
                "voterNo": False
            }
        })

    # Successful match simulation
    return {
        "status": "OK",
        "statusCode": "SUCCESS",
        "success": {
            "data": {
                "nationalId": "11111111111",
                "pin": "19973515187330207",
                "photo": "https://lh3.googleusercontent.com/a/ACg8ocJ88brxvS9EijBLcu4Mk1NwxNl3TBbQMkfjSqmlUtgRu1aVxXJR3A=s96-c-rg-br100"
            }
        },
        "verified": True,
        "fieldVerificationResult": {
            "mother": True,
            "permanentAddress.district": True,
            "father": True,
            "nameEn": True,
            "permanentAddress.division": True
        }
    }
