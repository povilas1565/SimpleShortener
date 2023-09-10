import typing as t


def generate_success_json(
    shortened_url: str, original_url: str
) -> t.Dict[t.Union[str, list], str]:
    """Generate json(dict) containing inforamtion about success status.
    :shortened_url: and :original_url: have to be passed.
    """

    success_json = {
        "status": "success",
        "data": [
            {
                "shortened_url": shortened_url,
                "original_url": original_url,
            },
        ],
    }
    return success_json


error_400_json = {
    "errors": [
        {
            "status": "error",
            "message": "Passed URL is not valid.",
        }
    ],
}

error_404_json = {
    "errors": [
        {
            "status": "error",
            "message": "Requested URL is not found.",
        }
    ],
}
