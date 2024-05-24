class Field:
    def __init__(self, unique=False):
        self.unique = unique

    def validate(self, value):
        raise NotImplementedError("Subclasses must implement validate method")

class CharField(Field):
    def __init__(self, max_length, unique=False):
        super().__init__(unique=unique)
        self.max_length = max_length

    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError("Value must be a string")
        if len(value) > self.max_length:
            raise ValueError(f"Value exceeds max_length of {self.max_length}")
        if self.unique:
            if value in self._unique_values:
                raise ValueError("Value must be unique")
            self._unique_values.add(value)

    # Track unique values for the sake of this example
    _unique_values = set()

class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        # Collect fields from class definition
        fields = {key: value for key, value in attrs.items() if isinstance(value, Field)}
        for key in fields.keys():
            attrs.pop(key)
        attrs['_fields'] = fields
        return super().__new__(cls, name, bases, attrs)

class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.validate_fields()

    def validate_fields(self):
        for key, field in self._fields.items():
            value = getattr(self, key, None)
            field.validate(value)

# Example usage
class User(Model):
    username = CharField(max_length=255, unique=True)
    email = CharField(max_length=100, unique=True)

try:
    user1 = User(username="john_doe", email="john@example.com")
    user2 = User(username="john_doe", email="john2@example.com")  # This should raise a ValueError
except ValueError as e:
    print(e)

