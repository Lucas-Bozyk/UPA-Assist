from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(max_length=20, choices=[('developer', 'Developer'), ('company', 'Company')], default='developer'),
        ),
    ]
