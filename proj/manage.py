#!/usr/bin/env python
import os
import sys
import yaml



if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test1.settings")

    from django.core.management import execute_from_command_line
    from django.core.management import call_command
    from django.db import models
    from django.contrib.admin import site
    from django.contrib.auth.models import User
    from django.db import connection as _conn
    from south.db import db as _south_db

    cur = _conn.cursor()

    stream = open("description.yaml", 'r')
    description = yaml.load(stream)

    for model_name, model_description in description.iteritems():
        if 'test1_%s' % model_name in _conn.introspection.get_table_list(cur):
            field_set = _conn.introspection.get_table_description(
                cur, 'test1_%s' % model_name
            )
            field_set = map(lambda x: (x[0], x[1]), field_set)
            field_set.remove(('id', 'integer'))
        else:
            field_set = None

        class Meta:
            pass

        setattr(Meta, 'app_label', 'test1')
        setattr(Meta, 'verbose_name', model_description['title'])

        fields = dict()

        for field in model_description['fields']:
            pair = (
                field['id'],
                {
                    'int': 'integer',
                    'char': 'varchar(128)',
                    'date': 'date'
                }.get(
                    (field['type'])
                )
            )

            if field_set and pair in field_set:
                field_set.remove(pair)
            elif field_set is not None and pair not in field_set:
                _south_db.add_column(
                    'test1_%s' % model_name,
                    field['id'],
                    {
                        'int': models.IntegerField(
                            blank=True, null=True
                        ),
                        'char': models.CharField(
                            max_length=128, blank=True, null=True
                        ),
                        'date': models.DateField(
                            blank=True, null=True
                        )
                    }.get(field['type'])
                )

            fields.update(
                {
                    field['id']: {
                        'int': models.IntegerField(
                            blank=True, null=True, verbose_name=field['title']
                        ),
                        'char': models.CharField(
                            max_length=128, blank=True, null=True,
                            verbose_name=field['title']
                        ),
                        'date': models.DateField(
                            blank=True, null=True, verbose_name=field['title']
                        )
                    }.get(field['type'])
                })
        if field_set:
            for to_remove in field_set:
                _south_db.delete_column('test1_%s' % model_name, to_remove[0])

        attrs = {'__module__': 'test1', 'Meta': Meta}
        attrs.update(fields)
        attrs.update({'get_meta': lambda self: self._meta})

        model = type(model_name, (models.Model,), attrs)
        site.register(model)

    call_command('syncdb', plain=True, interactive=False)
    try:
        call_command('schemamigration', initial=True, app='test1')
        call_command('migrate', app="test1", plain=True, interactive=False)
    except:
        pass

    if not User.objects.filter(username="root"):
        User.objects.create_superuser(
            username="root", email="root@root.com", password="root"
        )

    execute_from_command_line(sys.argv)