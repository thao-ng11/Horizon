# Generated by Django 4.2.1 on 2023-05-24 06:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_city"),
    ]

    operations = [
        migrations.CreateModel(
            name="Conditions",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "selector",
                    models.CharField(
                        choices=[
                            ("thunderstorm", "Thunderstorm"),
                            ("drizzle", "Drizzle"),
                            ("rain", "Rain"),
                            ("snow", "Snow"),
                            ("atmosphere", "Atmosphere"),
                            ("clear", "Clear"),
                            ("clouds", "Clouds"),
                        ],
                        default="thunderstorm",
                        max_length=12,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="WeatherConditions",
        ),
        migrations.AddField(
            model_name="city",
            name="state",
            field=models.CharField(default="New York", max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="city",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]