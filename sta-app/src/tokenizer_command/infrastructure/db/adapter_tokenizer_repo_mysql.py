import pymysql
from domain.model_tokenized_data import MedicalRecord
from domain.port_tokenizer_repo import ITokenizerRepository

class TokenizerRepository(ITokenizerRepository):
    def __init__(self):
        self.connection = pymysql.connect(
            host='0.0.0.0',
            user='admin',
            password='admin',
            database='tokenizer_command_db'
        )
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS medical_records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                image TEXT,
                diagnosis TEXT,
                report TEXT,
                body_part TEXT,
                modality TEXT,
                age TEXT,
                sex TEXT,
                ethnicity TEXT,
                symptoms TEXT,
                clinical_history TEXT,
                findings TEXT,
                impression TEXT,
                recommendation TEXT,
                indication TEXT,
                comparison TEXT,
                technique TEXT,
                no_finding TEXT,
                normal TEXT,
                abnormal TEXT,
                uncertain TEXT,
                other TEXT,
                unknown TEXT,
                code TEXT,
                diagnosis_date TEXT
            )
        ''')
        self.connection.commit()

    def insert_record(self, record: MedicalRecord):
        with self.connection.cursor() as cursor:
            cursor.execute('''
                INSERT INTO medical_records (
                    image, diagnosis, report, body_part, modality, age, sex, ethnicity, symptoms, clinical_history, findings, impression, recommendation, indication, comparison, technique, no_finding, normal, abnormal, uncertain, other, unknown, code, diagnosis_date
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (
                record.image, record.diagnosis, record.report, record.body_part, record.modality, record.age, record.sex, record.ethnicity, record.symptoms, record.clinical_history, record.findings, record.impression, record.recommendation, record.indication, record.comparison, record.technique, record.no_finding, record.normal, record.abnormal, record.uncertain, record.other, record.unknown, record.code, record.diagnosis_date.isoformat()
            ))
            self.connection.commit()

    def get_all_records(self):
        self.cursor.execute('SELECT * FROM medical_records')
        rows = self.cursor.fetchall()
        return [MedicalRecord(*row[1:]) for row in rows]