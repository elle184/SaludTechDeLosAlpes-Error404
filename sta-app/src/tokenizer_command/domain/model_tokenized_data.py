from dataclasses import dataclass
from datetime import datetime

@dataclass
class MedicalRecord:
    image: str
    diagnosis: str
    report: str
    body_part: str
    modality: str
    age: str
    sex: str
    ethnicity: str
    symptoms: str
    clinical_history: str
    findings: str
    impression: str
    recommendation: str
    indication: str
    comparison: str
    technique: str
    no_finding: str
    normal: str
    abnormal: str
    uncertain: str
    other: str
    unknown: str
    code: str
    diagnosis_date: datetime

    def to_json(self):
        return {
            "image": self.image,
            "diagnosis": self.diagnosis,
            "report": self.report,
            "body_part": self.body_part,
            "modality": self.modality,
            "age": self.age,
            "sex": self.sex,
            "ethnicity": self.ethnicity,
            "symptoms": self.symptoms,
            "clinical_history": self.clinical_history,
            "findings": self.findings,
            "impression": self.impression,
            "recommendation": self.recommendation,
            "indication": self.indication,
            "comparison": self.comparison,
            "technique": self.technique,
            "no_finding": self.no_finding,
            "normal": self.normal,
            "abnormal": self.abnormal,
            "uncertain": self.uncertain,
            "other": self.other,
            "unknown": self.unknown,
            "code": self.code,
            "diagnosis_date": self.diagnosis_date.isoformat()
        }

