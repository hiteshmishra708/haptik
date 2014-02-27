from django.db import models


class Collections(models.Model):
    prev_id = models.IntegerField(null=True);
    next_id = models.IntegerField(null=True);
    us = models.CharField(max_length=2047, null=True)
    with_user = models.CharField(max_length=1023, null=True)
    with_server = models.CharField(max_length=1023, null=True)
    with_resource = models.CharField(max_length=1023, null=True)
    utc = models.DateTimeField(null=True)
    change_by = models.CharField(max_length=3071, null=True)
    change_utc = models.DateTimeField(null=True);
    deleted =  models.BooleanField(null=True)
    subject = models.CharField(max_length=1023,null=True)
    thread = models.CharField(max_length=1023, null=True)
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
