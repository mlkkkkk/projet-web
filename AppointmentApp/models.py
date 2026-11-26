from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone


class Status(models.TextChoices):
    PENDING = "PENDING", "En attente"
    CONFIRMED = "CONFIRMED", "Confirmé"
    CANCELLED = "CANCELLED", "Annulé"


class Appointment(models.Model):
    reason = models.TextField()
    prescription = models.FileField(
        upload_to="prescriptions/",
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    duration_minutes = models.PositiveIntegerField(default=30)
    appointment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    doctor = models.ForeignKey(
        "AccountApp.Doctor", on_delete=models.CASCADE, related_name="appointments"
    )
    patient = models.ForeignKey(
        "AccountApp.Patient", on_delete=models.CASCADE, related_name="appointments"
    )

    class Meta:
        ordering = ["appointment_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointment_date"],
                name="unique_doctor_appointment_date",
                violation_error_message="Ce médecin a déjà un rendez-vous à cette date.",
            )
        ]

    def clean(self):
        modified_date = self._state.adding or (
            not Appointment.objects.filter(
                pk=self.pk, appointment_date=self.appointment_date
            ).exists()
        )
        if modified_date and self.appointment_date <= timezone.now():
            raise ValidationError(
                "La date du rdv doit être postérieure à la date d'aujourd'hui."
            )

    def __str__(self):
        return f"Rendez-vous pour raion {self.reason}"