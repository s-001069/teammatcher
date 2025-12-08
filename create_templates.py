from teacher_side.models import TeamNameTemplate

marvel_template = TeamNameTemplate.objects.create(
    name="Marvel Heroes",
    team_names=[
        "Avengers",
        "X-Men",
        "Guardians of the Galaxy",
        "Fantastic Four",
        "Defenders"
    ],
    is_default=True
)
print(f"Created: {marvel_template}")

greek_template = TeamNameTemplate.objects.create(
    name="Greek Gods",
    team_names=[
        "Zeus",
        "Athena",
        "Poseidon",
        "Apollo",
        "Artemis"
    ]
)
print(f"Created: {greek_template}")

color_template = TeamNameTemplate.objects.create(
    name="Color Teams",
    team_names=[
        "Red Dragons",
        "Blue Phoenixes",
        "Green Titans",
        "Yellow Lightning",
        "Purple Warriors"
    ]
)
print(f"Created: {color_template}")

print("\nAll templates created successfully!")
print(f"Total templates: {TeamNameTemplate.objects.count()}")
