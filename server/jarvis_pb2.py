# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: jarvis.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cjarvis.proto\x12\x06server\"\x9c\x01\n\x08TaskInfo\x12\x0f\n\x07task_id\x18\x01 \x01(\x05\x12\x0c\n\x04task\x18\x02 \x01(\t\x12\x0e\n\x06result\x18\x03 \x01(\t\x12\x30\n\x08metadata\x18\x04 \x03(\x0b\x32\x1e.server.TaskInfo.MetadataEntry\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"h\n\x0e\x45xecuteRequest\x12\x0f\n\x07task_id\x18\x01 \x01(\x05\x12\x0c\n\x04task\x18\x02 \x01(\t\x12\x0c\n\x04goal\x18\x03 \x01(\t\x12)\n\x0f\x64\x65pendent_tasks\x18\x04 \x03(\x0b\x32\x10.server.TaskInfo\"O\n\x0f\x45xecuteResponse\x12\x0f\n\x07task_id\x18\x01 \x01(\x05\x12\x0c\n\x04task\x18\x02 \x01(\t\x12\x0e\n\x06result\x18\x03 \x01(\t\x12\r\n\x05\x65rror\x18\x04 \x01(\t2D\n\x06Jarvis\x12:\n\x07\x45xecute\x12\x16.server.ExecuteRequest\x1a\x17.server.ExecuteResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'jarvis_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TASKINFO_METADATAENTRY._options = None
  _TASKINFO_METADATAENTRY._serialized_options = b'8\001'
  _globals['_TASKINFO']._serialized_start=25
  _globals['_TASKINFO']._serialized_end=181
  _globals['_TASKINFO_METADATAENTRY']._serialized_start=134
  _globals['_TASKINFO_METADATAENTRY']._serialized_end=181
  _globals['_EXECUTEREQUEST']._serialized_start=183
  _globals['_EXECUTEREQUEST']._serialized_end=287
  _globals['_EXECUTERESPONSE']._serialized_start=289
  _globals['_EXECUTERESPONSE']._serialized_end=368
  _globals['_JARVIS']._serialized_start=370
  _globals['_JARVIS']._serialized_end=438
# @@protoc_insertion_point(module_scope)
