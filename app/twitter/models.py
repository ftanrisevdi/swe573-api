from django.db import models


class Twit(models.Model):
    
    search_key_word = models.CharField(max_length=100) 
    created = models.DateTimeField()
    clean_twits =models.JSONField() 
    cooked =  models.JSONField()
    word_count = models.JSONField()
    twits = models.JSONField()
    user_id = models.CharField(max_length=255)
    

    def __str__(self):
        return self.id

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "result"