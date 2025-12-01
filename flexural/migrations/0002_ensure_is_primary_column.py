from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flexural', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE flexural_calculation_item ADD COLUMN IF NOT EXISTS is_primary boolean DEFAULT FALSE",
            reverse_sql="ALTER TABLE flexural_calculation_item DROP COLUMN IF EXISTS is_primary",
        ),
        migrations.RunSQL(
            sql="UPDATE flexural_calculation_item SET is_primary = COALESCE(is_primary, FALSE)",
            reverse_sql=migrations.RunSQL.noop,
        ),
        migrations.RunSQL(
            sql="ALTER TABLE flexural_calculation_item ALTER COLUMN is_primary SET NOT NULL",
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
