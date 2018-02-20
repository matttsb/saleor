import graphene

from ...dashboard.category.forms import CategoryForm
from ...product import models
from ..core.types import ErrorType
from .types import Category


def convert_form_errors(form):
    """Convert ModelForm errors into a list of ErrorType objects"""
    errors = []
    for field in form.errors:
        for message in form.errors[field]:
            errors.append(ErrorType(field=field, message=message))
    return errors


class CategoryMutation(graphene.Mutation):
    category = graphene.Field(Category)
    errors = graphene.List(ErrorType)

    def mutate(self, info):
        raise NotImplementedError


class CategoryInput(graphene.InputObjectType):
    name = graphene.String()
    description = graphene.String()
    parent = graphene.ID()


class CategoryCreate(CategoryMutation):
    class Arguments:
        data = CategoryInput()

    def mutate(self, info, data):
        category = models.Category()
        errors = []
        parent_id = data.pop('parent', None)
        if parent_id:
            parent = graphene.Node.get_node_from_global_id(
                info, parent_id, only_type=Category)
        else:
            parent = None
        parent_pk = parent.pk if parent else None
        form = CategoryForm(data, instance=category, parent_pk=parent_pk)
        if form.is_valid():
            category = form.save()
        else:
            errors = convert_form_errors(form)
        return CategoryCreate(category=category, errors=errors)


class CategoryUpdate(CategoryMutation):
    class Arguments:
        data = CategoryInput()
        id = graphene.ID()

    def mutate(self, info, data, id):
        category = graphene.Node.get_node_from_global_id(
            info, id, only_type=Category)
        errors = []
        if category:
            form = CategoryForm(
                data, instance=category, parent_pk=category.parent_id)
            if form.is_valid():
                category = form.save()
            else:
                errors = convert_form_errors(form)
        return CategoryCreate(category=category, errors=errors)


class CategoryDelete(CategoryMutation):
    class Arguments:
        id = graphene.ID()

    def mutate(self, info, id):
        category = graphene.Node.get_node_from_global_id(
            info, id, only_type=Category)
        if category:
            category.delete()
        return CategoryCreate(category=category)
