from api.helpers.apis import handle_error_response
from flask import request


def paginate(query, schema) -> dict:
    """Return the paginated data based on the request

    Args:
        query (object): the SQLALCHEMY query in order to paginate the data
        schema (object): The schema of the selected model in order to deserialize the data

    Returns:
        object: {
            total_items,
            pages,
            page,
            items,
            num_rows,
        }
    """
    # * the number of pages which is requested
    page = request.args.get("page", type=int, default=1)
    page = int(page)

    # ? How many rows we want for each page
    per_page = request.args.get("page_size", type=int, default=10)

    # ! check the validation of number of rows
    if per_page <= 0:
        return handle_error_response(
            type="PaginationError",
            code=15,
            sub_code=100,
            mimetype="application/json",
            status=400,
            msg="number of rows is not valid",
        )

    per_page = int(per_page)

    # * Have a paginated query.
    page_obj = query.paginate(page=page, per_page=per_page, error_out=False)

    response_data = {
        "total_items": page_obj.total,
        "pages": page_obj.pages,
        "page": page_obj.page,
        "items": schema.dump(page_obj.items),
        "num_rows": per_page,
    }

    if len(schema.dump(page_obj.items)) == 0:
        page = 1
        page_obj = query.paginate(page=page, per_page=per_page, error_out=False)

        response_data = {
            "total_items": page_obj.total,
            "pages": page_obj.pages,
            "page": page_obj.page,
            "items": schema.dump(page_obj.items),
            "num_rows": per_page,
        }

    return response_data
