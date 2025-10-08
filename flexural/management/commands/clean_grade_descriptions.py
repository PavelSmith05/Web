import re
from django.core.management.base import BaseCommand
from flexural.models import ConcreteGrade

PATTERN = re.compile(r"\.?\s*Коэффициент\s+прочности\s+—?\s*[0-9]+(?:\.[0-9]+)?\.?$", re.IGNORECASE)

class Command(BaseCommand):
    help = "Очистить descriptions марок бетона от хвоста 'Коэффициент прочности — X'. По умолчанию dry-run."

    def add_arguments(self, parser):
        parser.add_argument("--apply", action="store_true", help="Сохранить изменения (по умолчанию только показать diff)")
        parser.add_argument("--filter", dest="grade_codes", nargs="*", help="Ограничить конкретными grade_code")

    def handle(self, *args, **options):
        apply = options["apply"]
        grade_codes = options.get("grade_codes")
        qs = ConcreteGrade.objects.all()
        if grade_codes:
            qs = qs.filter(grade_code__in=grade_codes)
        changed = 0
        for g in qs.order_by("id"):
            original = g.description or ""
            new = PATTERN.sub("", original).strip()
            # Удаляем двойные точки и пробелы в конце
            new = re.sub(r"[\s\.]+$", "", new)
            if new != original:
                changed += 1
                self.stdout.write(self.style.WARNING(f"{g.grade_code}:"))
                self.stdout.write(f"  OLD: {original}")
                self.stdout.write(f"  NEW: {new}")
                if apply:
                    g.description = new
                    g.save(update_fields=["description"])
        if changed == 0:
            self.stdout.write(self.style.SUCCESS("Нет записей требующих очистки."))
        else:
            if apply:
                self.stdout.write(self.style.SUCCESS(f"Обновлено {changed} описаний."))
            else:
                self.stdout.write(self.style.NOTICE(f"Найдено {changed} описаний для очистки. Запустите с --apply для сохранения."))
