from django.db import models
from school.models import StudentProfile, EmployeeProfile

# Create your models here.
class Deficiency(models.Model):
    deficiency_id = models.CharField(max_length=100, blank=True, null=True)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="student_with_deficiency")
    added_by = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, related_name="added_by")
    processed_by = models.ForeignKey(EmployeeProfile, on_delete=models.CASCADE, blank=True, null=True, related_name="processed_by")
    is_complete = models.BooleanField(default=False)
    date_fulfilled = models.DateField(default=None, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    name = models.CharField(max_length=100, default=None)
    category = models.CharField(max_length=100, default=None)

    def __str__(self):
        return f"{self.student} has a deficiency in {self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        prefix = "O"

        if self.category == "Finance":
            prefix = "F"
        if self.category == "Document":
            prefix = "D"

        self.deficiency_id = prefix + str(self.pk).zfill(7)

        super().save(*args, **kwargs)


class FinanceDeficiency(models.Model):
    deficiency = models.OneToOneField(Deficiency, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=9)

    def __str__(self):
        return f"Balance of: {str(self.amount)}"

class DocumentDeficiency(models.Model):
    deficiency = models.OneToOneField(Deficiency, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=100)

    def __str__(self):
        return self.document_type