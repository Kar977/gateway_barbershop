from pydantic import BaseModel


class CreateScheduleRequest(BaseModel):
    employee_id: str
    full_name: str
    day: str
    availability: str


class UpdateScheduleRequest(BaseModel):
    employee_id: str
    schedule_id: int
    new_availability: str


class DeleteScheduleRequest(BaseModel):
    employee_id: str
    schedule_id: int
