"""
This namespace defines the DBFunction abstract class and its subclasses. These subclasses
represent functions that have identifiers, display names and hints, and their instances
hold parameters. Each DBFunction subclass defines how its instance can be converted into an
SQLAlchemy expression.

Hints hold information about what kind of input the function might expect and what output
can be expected from it. This is used to provide interface information without constraining its
user.

These classes might be used, for example, to define a filter for an SQL query, or to
access hints on what composition of functions and parameters should be valid.
"""

from abc import ABC, abstractmethod

from sqlalchemy import column, not_, and_, or_, func, literal

from db.functions import hints
from db.functions.exceptions import BadDBFunctionFormat, UseOfColumnIDInSAExpression, ReferencedColumnsDontExist


# NOTE: this class is abstract.
class DBFunction(ABC):
    id = None
    name = None
    hints = None

    # Optionally lists the SQL functions this DBFunction depends on.
    # Will be checked against SQL functions defined on a database to tell if it
    # supports this DBFunction. Either None or a tuple of SQL function name
    # strings.
    depends_on = None

    def __eq__(self, other):
        return (
            isinstance(other, DBFunction)
            and self.id == other.id
            and self.parameters == other.parameters
        )

    def __init__(self, parameters):
        if self.id is None:
            raise ValueError('DBFunction subclasses must define an ID.')
        if self.name is None:
            raise ValueError('DBFunction subclasses must define a name.')
        if self.depends_on is not None and not isinstance(self.depends_on, tuple):
            raise ValueError('DBFunction subclasses\' depends_on attribute must either be None or a tuple of SQL function names.')
        if not isinstance(parameters, list):
            raise BadDBFunctionFormat('DBFunction instance parameter `parameters` must be a list.')
        self.parameters = parameters

    @property
    def referenced_columns(self):
        """Walks the expression tree, collecting referenced columns.
        Useful when checking if all referenced columns are present in the queried relation."""
        columns = set([])
        for parameter in self.parameters:
            if isinstance(parameter, ColumnReference):
                columns.add(parameter.column)
            elif isinstance(parameter, DBFunction):
                columns.update(parameter.referenced_columns)
        return columns

    @staticmethod
    @abstractmethod
    def to_sa_expression():
        return None


class Literal(DBFunction):
    id = 'literal'
    name = 'as literal'
    hints = tuple([
        hints.parameter_count(1),
        hints.parameter(1, hints.literal),
    ])

    @staticmethod
    def to_sa_expression(primitive):
        return literal(primitive)


# NOTE: this class is abstract.
class ColumnReference(DBFunction):
    hints = tuple([
        hints.parameter_count(1),
        hints.parameter(1, hints.column),
    ])

    @property
    def column(self):
        return self.parameters[0]


# This represents referencing columns by their Django ID.
# It cannot be used to create an SQLAlchemy expression, see ColumnName.
# The system is expected to convert id references to name references automatically.
class ColumnID(ColumnReference):
    id = 'column_id'
    name = 'as column id'

    def to_column_name(self, column_ids_to_names):
        column_id = self.column
        column_name = column_ids_to_names.get(column_id, None)
        if column_name:
            return ColumnName([column_name])
        else:
            raise ReferencedColumnsDontExist(
                f"Column name corresponding to referenced column id {column_id} unknown."
                + f" Known id-to-name mapping: {column_ids_to_names}"
            )

    @staticmethod
    def to_sa_expression(_):
        # DBFunction can be converted into an SA expression.
        raise UseOfColumnIDInSAExpression


# This represents referencing columns by their Postgres name.
class ColumnName(ColumnReference):
    id = 'column_name'
    name = 'as column name'

    @staticmethod
    def to_sa_expression(column_name):
        return column(column_name)


class List(DBFunction):
    id = 'list'
    name = 'as list'

    @staticmethod
    def to_sa_expression(*items):
        return list(items)


class Empty(DBFunction):
    id = 'empty'
    name = 'is empty'
    hints = tuple([
        hints.returns(hints.boolean),
        hints.parameter_count(1),
        hints.parameter(0, hints.any),
        hints.mathesar_filter,
    ])

    @staticmethod
    def to_sa_expression(value):
        return value.is_(None)


class Not(DBFunction):
    id = 'not'
    name = 'negate'
    hints = tuple([
        hints.returns(hints.boolean),
    ])

    @staticmethod
    def to_sa_expression(*values):
        length = len(values)
        if length > 1:
            return not_(and_(*values))
        else:
            return not_(values[0])


class Equal(DBFunction):
    id = 'equal'
    name = 'is equal to'
    hints = tuple([
        hints.returns(hints.boolean),
        hints.parameter_count(2),
        hints.all_parameters(hints.any),
        hints.mathesar_filter,
    ])

    @staticmethod
    def to_sa_expression(value1, value2):
        return value1 == value2


class Greater(DBFunction):
    id = 'greater'
    name = 'is greater than'
    hints = tuple([
        hints.returns(hints.boolean),
        hints.parameter_count(2),
        hints.all_parameters(hints.comparable),
        hints.mathesar_filter,
    ])

    @staticmethod
    def to_sa_expression(value1, value2):
        return value1 > value2


class Lesser(DBFunction):
    id = 'lesser'
    name = 'is lesser than'
    hints = tuple([
        hints.returns(hints.boolean),
        hints.parameter_count(2),
        hints.all_parameters(hints.comparable),
        hints.mathesar_filter,
    ])

    @staticmethod
    def to_sa_expression(value1, value2):
        return value1 < value2


class In(DBFunction):
    id = 'in'
    name = 'is in'
    hints = tuple([
        hints.returns(hints.boolean),
        hints.parameter_count(2),
        hints.parameter(2, hints.array),
    ])

    @staticmethod
    def to_sa_expression(value1, value2):
        return value1.in_(value2)


class And(DBFunction):
    id = 'and'
    name = 'and'
    hints = tuple([
        hints.returns(hints.boolean),
    ])

    @staticmethod
    def to_sa_expression(*values):
        return and_(*values)


class Or(DBFunction):
    id = 'or'
    name = 'or'
    hints = tuple([
        hints.returns(hints.boolean),
    ])

    @staticmethod
    def to_sa_expression(*values):
        return or_(*values)


class StartsWith(DBFunction):
    id = 'starts_with'
    name = 'starts with'
    hints = tuple([
        hints.returns(hints.boolean),
        hints.parameter_count(2),
        hints.all_parameters(hints.string_like),
        hints.mathesar_filter,
    ])

    @staticmethod
    def to_sa_expression(string, prefix):
        return string.like(f'{prefix}%')


class ToLowercase(DBFunction):
    id = 'to_lowercase'
    name = 'to lowercase'
    hints = tuple([
        hints.returns(hints.string_like),
        hints.parameter_count(1),
        hints.all_parameters(hints.string_like),
        hints.mathesar_filter,
    ])

    @staticmethod
    def to_sa_expression(string):
        return func.lower(string)