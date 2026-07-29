from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class ScenesResponse(BaseModel):
    scenes: list[str]


class MetricsResponse(BaseModel):
    threshold: int
    changedPixels: int
    totalPixels: int
    changeRatio: float
    note: str


class ProcessingReportInputs(BaseModel):
    before: str
    after: str


class ProcessingReportParameters(BaseModel):
    threshold: int
    normalization: str


class ProcessingReportWarning(BaseModel):
    type: str
    message: str
    beforeShape: list[int]
    afterShape: list[int]


class ProcessingReportValidation(BaseModel):
    sameShape: bool
    warnings: list[ProcessingReportWarning]


class ProcessingReportOutputs(BaseModel):
    beforePng: str
    afterPng: str
    diffPng: str
    maskPng: str
    metricsJson: str
    processingReportJson: str


class ProcessingReportMetrics(BaseModel):
    changedPixels: int
    totalPixels: int
    changeRatio: float


class ProcessingReportResponse(BaseModel):
    sceneId: str
    inputs: ProcessingReportInputs
    parameters: ProcessingReportParameters
    validation: ProcessingReportValidation
    outputs: ProcessingReportOutputs
    metrics: ProcessingReportMetrics
    note: str
