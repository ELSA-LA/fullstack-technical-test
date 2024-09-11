# Generated by Django 4.2 on 2024-09-05 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("albergue", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Usuario",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("nombre", models.CharField(max_length=100)),
                ("apellido", models.CharField(max_length=100)),
                (
                    "rol",
                    models.CharField(
                        choices=[
                            ("V", "Voluntario"),
                            ("A", "Adoptante"),
                            ("S", "Administrador"),
                        ],
                        max_length=1,
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to.",
                        related_name="usuario_groups",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="usuario_permissions",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AlterField(
            model_name="adopcion",
            name="adoptador",
            field=models.ForeignKey(
                limit_choices_to={"rol": "A"},
                on_delete=django.db.models.deletion.CASCADE,
                related_name="adopciones_adoptador",
                to="albergue.usuario",
            ),
        ),
        migrations.AlterField(
            model_name="adopcion",
            name="voluntario",
            field=models.ForeignKey(
                limit_choices_to={"rol": "V"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="adopciones_voluntario",
                to="albergue.usuario",
            ),
        ),
        migrations.AlterField(
            model_name="animal",
            name="voluntario",
            field=models.ForeignKey(
                limit_choices_to={"rol": "V"},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="animales",
                to="albergue.usuario",
            ),
        ),
        migrations.DeleteModel(
            name="Adoptador",
        ),
        migrations.DeleteModel(
            name="Voluntario",
        ),
    ]