def convert_unit(value, from_unit, to_unit):
    return {
        ("miles", "km"): lambda x: x * 1.60934,
        ("km", "miles"): lambda x: x / 1.60934,
    }.get(
        (from_unit, to_unit),
        lambda x: (_ for _ in ()).throw(ValueError("Conversion not supported.")),
    )(
        value
    )
