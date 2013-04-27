from django.db import models


class Collections(models.Model):
    prev_id = models.IntegerField();
    next_id = models.IntegerField();
    us = models.CharField(max_length=2047)
    with_user = models.CharField(max_length=1023)
    with_server = models.CharField(max_length=1023)
    with_resource = models.CharField(max_length=1023, null=True)
    utc = models.DateTimeField()
    change_by = models.CharField(max_length=3071)
    change_utc = models.DateTimeField();
    deleted =  models.BooleanField()
    subject = models.CharField(max_length=1023)
    thread = models.CharField(max_length=1023)
    crypt = models.BooleanField(null=True)
    extra = models.TextField(null=True)

    def __unicode__(self):
        return unicode_class(self)

    def to_dict(self):
        return convert_to_dict(self)

    class Meta:
        db_table = 'archive_collections'


class Messages(models.Model):
    coll = models.ForeignKey(Collections)#models.IntegerField()
    utc = models.DateTimeField()
    dir = models.BooleanField()
    body = models.TextField()
    name = models.CharField(max_length=1023, null=True)
    

    def __unicode__(self):
        return unicode_class(self)

    def to_dict(self):
        return convert_to_dict(self)

    class Meta:
        db_table = 'archive_messages'




def unicode_class(obj):
    s = ''
    for k,v in obj.__dict__.items():
        s += ('%s: %s\n' % (k,v))
    return s


def convert_to_dict(obj):
    return obj.__dict__
