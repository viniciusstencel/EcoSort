from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AiClassificationRequest(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class AiClassificationResponse(_message.Message):
    __slots__ = ("class_id", "class_name", "confidence")
    CLASS_ID_FIELD_NUMBER: _ClassVar[int]
    CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    class_id: int
    class_name: str
    confidence: float
    def __init__(self, class_id: _Optional[int] = ..., class_name: _Optional[str] = ..., confidence: _Optional[float] = ...) -> None: ...
