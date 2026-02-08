import functools
import inspect
from typing import Any, Callable, Dict, List, Optional, get_type_hints, get_origin, get_args
from enum import Enum
from pydantic import BaseModel

class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    SYSTEM = "system"

class Message(BaseModel):
    role: Role
    content: str
    name: Optional[str] = None
    tool_call_id: Optional[str] = None
    base64_image: Optional[str] = None

    @classmethod
    def tool_message(
        cls, content: str, name: str, tool_call_id: str, base64_image: Optional[str] = None
    ) -> "Message":
        """Create a tool message"""
        return cls(
            role=Role.TOOL,
            content=content,
            name=name,
            tool_call_id=tool_call_id,
            base64_image=base64_image,
        )

class ToolRegistry:
    def __init__(self):
        self.tools = {}
        self.tool_implementations = {}

    def tool(self):
        """Create a decorator for a function as an MCP tool.
        Uses function name, docstring, and type hints to generate the MCP tool schema.
        """
        def decorator(func: Callable):
            # Get function name
            tool_name = func.__name__

            # Get docstring and parse into description
            doc = inspect.getdoc(func) or ''
            description = doc.split('\n\n')[0]

            # Get type hints
            hints = get_type_hints(func)
            hints.pop('return', Any)

            # Build input schema from type hints
            properties = {}
            required = []

            # Parse docstring for argument descriptions
            arg_descriptions = {}
            if doc:
                lines = doc.split('\n')
                in_args = False
                for line in lines:
                    if line.strip().startswith('Args:'):
                        in_args = True
                        continue
                    if in_args:
                        if not line.strip() or line.strip().startswith('Returns:'):
                            break
                        if ':' in line:
                            arg_name, arg_desc = line.split(':', 1)
                            arg_descriptions[arg_name.strip()] = arg_desc.strip()

            def get_type_schema(type_hint: Any) -> Dict[str, Any]:
                if type_hint is int: return {'type': 'integer'}
                elif type_hint is float: return {'type': 'number'}
                elif type_hint is bool: return {'type': 'boolean'}
                elif type_hint is str: return {'type': 'string'}
                
                if isinstance(type_hint, type) and issubclass(type_hint, Enum):
                    return {'type': 'string', 'enum': [e.value for e in type_hint]}

                origin = get_origin(type_hint)
                if origin is list or origin is List:
                    args = get_args(type_hint)
                    item_schema = get_type_schema(args[0]) if args else {}
                    return {'type': 'array', 'items': item_schema}
                
                return {'type': 'string'}

            for param_name, param_type in hints.items():
                if param_name == "user_id": continue # Internal param
                param_schema = get_type_schema(param_type)
                if param_name in arg_descriptions:
                    param_schema['description'] = arg_descriptions[param_name]
                properties[param_name] = param_schema
                required.append(param_name)

            tool_schema = {
                'name': tool_name,
                'description': description,
                'inputSchema': {'type': 'object', 'properties': properties, 'required': required},
            }

            self.tools[tool_name] = tool_schema
            self.tool_implementations[tool_name] = func

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

registry = ToolRegistry()
tool = registry.tool