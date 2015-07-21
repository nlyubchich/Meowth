from flask import Blueprint, render_template, url_for
from project.admin.forms import VacancyForm, CategoryForm, CityForm
from project.pages.forms import PageBlockForm, PageForm
from project.admin.utils import EntryDetail, EntryList
from project.auth.forms import RegisterForm, UserEditForm
from project.models import Vacancy, Category, City, User, PageBlock, Page

SECTIONS = {}  # list_name: list_endpoint


admin_app = Blueprint('admin', __name__)


def register_section(*, section_name, list_endpoint,
                     list_route, detail_route,
                     list_view, detail_view):

    admin_app.add_url_rule(list_route, view_func=list_view)

    admin_app.add_url_rule(
        detail_route+"<int:entry_id>/",
        view_func=detail_view,
    )

    admin_app.add_url_rule(
        detail_route,
        defaults={'entry_id': None},
        view_func=detail_view,
    )

    SECTIONS[section_name] = list_endpoint


# Vacancies
vacancy_list = EntryList.as_view(
    name='vacancy_list',
    model=Vacancy,
    template="admin/vacancies.html",
)

vacancy_detail = EntryDetail.as_view(
    name='vacancy_detail',
    create_form=VacancyForm,
    model=Vacancy,
    template="admin/vacancy.html",
    success_url="vacancy_list",
)

register_section(
    section_name="Вакансии",
    list_route="/vacancies/",
    detail_route="/vacancy/",
    list_view=vacancy_list,
    detail_view=vacancy_detail,
    list_endpoint="vacancy_list",
)


# Categories
category_list = EntryList.as_view(
    name="category_list",
    model=Category,
    template="admin/categories.html",
)


category_detail = EntryDetail.as_view(
    name='category_detail',
    create_form=CategoryForm,
    model=Category,
    success_url="category_list",
)

register_section(
    section_name="Категории",
    list_route="/categories/",
    detail_route="/category/",
    list_view=category_list,
    detail_view=category_detail,
    list_endpoint="category_list",
)


# Cities
city_list = EntryList.as_view(
    name="city_list",
    model=City,
    template="admin/cities.html",
)
city_view = EntryDetail.as_view(
    name='city_detail',
    create_form=CityForm,
    model=City,
    success_url="city_list",
)

register_section(
    section_name="Города",
    list_route="/cities/",
    detail_route="/city/",
    list_view=city_list,
    detail_view=city_view,
    list_endpoint="city_list",
)


# Users
user_list = EntryList.as_view(
    name="user_list",
    model=User,
    template="admin/users.html",
)

user_detail = EntryDetail.as_view(
    name='user_detail',
    create_form=RegisterForm,
    update_form=UserEditForm,
    model=User,
    success_url="user_list",
)

register_section(
    section_name="Пользователи",
    list_route="/users/",
    detail_route="/user/",
    list_view=user_list,
    detail_view=user_detail,
    list_endpoint="user_list",
)


# PageBlocks
@admin_app.route("/blocks/")
def pageblocks_list():
    return render_template(
        "admin/pageblocks.html",
        pageblocks=PageBlock.query.all(),
    )


@admin_app.route("/page/<int:p_id>/blocks/")
def pageblocks_for_page_list(p_id):
    return render_template(
        "admin/pageblocks.html",
        pageblocks=PageBlock.query
        .filter(PageBlock.page_id == p_id)
        .order_by(PageBlock.position.asc())
        .all(),
    )

pageblock_view = EntryDetail.as_view(
    name='pageblock_detail',
    create_form=PageBlockForm,
    model=PageBlock,
    success_url="pageblocks_list",
)

admin_app.add_url_rule(
    "/block/<int:entry_id>/",
    view_func=pageblock_view,
)


admin_app.add_url_rule(
    "/block/<int:entry_id>/",
    view_func=pageblock_view,
)

admin_app.add_url_rule(
    "/block",
    defaults={'entry_id': None},
    view_func=pageblock_view,
)


# Pages
@admin_app.route("/pages/")
def pages_list():
    return render_template(
        "admin/pages.html",
        pages=Page.query.all(),
    )

page_view = EntryDetail.as_view(
    name='page_detail',
    create_form=PageForm,
    model=Page,
    success_url="pages_list",
)

admin_app.add_url_rule(
    "/page/<int:entry_id>/",
    view_func=page_view,
)

admin_app.add_url_rule(
    "/page",
    defaults={'entry_id': None},
    view_func=page_view,
)


@admin_app.route("/")
def mainpage():
    sections = {}
    for name, endpoint in SECTIONS.items():
        sections[name] = url_for("admin."+endpoint)

    return render_template(
        "admin/main.html",
        sections=sections.items(),
    )
