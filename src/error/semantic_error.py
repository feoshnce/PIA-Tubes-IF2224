class SemanticError(Exception):
    def __init__(self, message: str, identifier: str = None):
        self.message = message
        self.identifier = identifier
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.identifier:
            return f"Semantic Error: {self.message} (identifier: '{self.identifier}')"
        return f"Semantic Error: {self.message}"


class UndeclaredIdentifierError(SemanticError):
    def __init__(self, identifier: str):
        super().__init__(f"Undeclared identifier '{identifier}'", identifier)


class DuplicateDeclarationError(SemanticError):
    def __init__(self, identifier: str):
        super().__init__(f"Duplicate declaration of '{identifier}'", identifier)


class TypeMismatchError(SemanticError):
    def __init__(self, expected: str, got: str, context: str = ""):
        msg = f"Type mismatch: expected {expected}, got {got}"
        if context:
            msg += f" in {context}"
        super().__init__(msg)


class InvalidOperationError(SemanticError):
    def __init__(self, operation: str, operand_type: str):
        super().__init__(f"Invalid operation '{operation}' for type {operand_type}")


class InvalidArrayIndexError(SemanticError):
    def __init__(self, message: str):
        super().__init__(f"Invalid array index: {message}")


class InvalidRecordAccessError(SemanticError):
    def __init__(self, record_name: str, field_name: str):
        super().__init__(f"Record '{record_name}' has no field '{field_name}'")


class InvalidFunctionCallError(SemanticError):
    def __init__(self, message: str):
        super().__init__(f"Invalid function call: {message}")
