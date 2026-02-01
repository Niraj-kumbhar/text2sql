import ast
import re


def tool_messages_to_documents_json(messages, tool_name=None):
    """
    Combine: filter tool messages from a mixed `messages` list and convert their
    `content` into documents of the form {"page_content": ..., "metadata": ...}.

    Args:
        messages: Iterable of message dicts or objects. Messages may have attributes
            or keys like `type` or `role` (to detect tool messages), `name`, and
            `content`.
        tool_name: Optional name to filter messages by their `name` field.

    Returns:
        List[dict]: documents extracted from tool message contents.
    """

    docs = []
    pattern = re.compile(
        r"metadata=(\{.*?\})\s*,\s*page_content=(['\"])(.*?)\2",
        flags=re.DOTALL,
    )

    for msg in messages:
        # determine message type/role, name, and content in both dict and object forms
        if isinstance(msg, dict):
            m_type = msg.get('type') or msg.get('role')
            name = msg.get('name') or msg.get('tool')
            content = msg.get('content')
        else:
            m_type = getattr(msg, 'type', None) or getattr(msg, 'role', None)
            name = getattr(msg, 'name', None)
            content = getattr(msg, 'content', None)

        if m_type != 'tool':
            continue

        if tool_name is not None and name != tool_name:
            continue

        if content is None:
            continue

        # Ensure we search in a string representation in case content is not str
        content_str = content if isinstance(content, str) else str(content)

        for meta_str, _, page_content in pattern.findall(content_str):
            metadata = ast.literal_eval(meta_str)
            docs.append({
                'page_content': page_content,
                'metadata': metadata,
            })

    return docs
