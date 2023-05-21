# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BatchJobExecution(models.Model):
    job_execution_id = models.BigIntegerField(db_column='JOB_EXECUTION_ID', primary_key=True)  # Field name made lowercase.
    version = models.BigIntegerField(db_column='VERSION', blank=True, null=True)  # Field name made lowercase.
    job_instance = models.ForeignKey('BatchJobInstance', models.DO_NOTHING, db_column='JOB_INSTANCE_ID')  # Field name made lowercase.
    create_time = models.DateTimeField(db_column='CREATE_TIME')  # Field name made lowercase.
    start_time = models.DateTimeField(db_column='START_TIME', blank=True, null=True)  # Field name made lowercase.
    end_time = models.DateTimeField(db_column='END_TIME', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    exit_code = models.CharField(db_column='EXIT_CODE', max_length=2500, blank=True, null=True)  # Field name made lowercase.
    exit_message = models.CharField(db_column='EXIT_MESSAGE', max_length=2500, blank=True, null=True)  # Field name made lowercase.
    last_updated = models.DateTimeField(db_column='LAST_UPDATED', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BATCH_JOB_EXECUTION'


class BatchJobExecutionContext(models.Model):
    job_execution = models.OneToOneField(BatchJobExecution, models.DO_NOTHING, db_column='JOB_EXECUTION_ID', primary_key=True)  # Field name made lowercase.
    short_context = models.CharField(db_column='SHORT_CONTEXT', max_length=2500)  # Field name made lowercase.
    serialized_context = models.TextField(db_column='SERIALIZED_CONTEXT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BATCH_JOB_EXECUTION_CONTEXT'


class BatchJobExecutionParams(models.Model):
    job_execution = models.ForeignKey(BatchJobExecution, models.DO_NOTHING, db_column='JOB_EXECUTION_ID')  # Field name made lowercase.
    parameter_name = models.CharField(db_column='PARAMETER_NAME', max_length=100)  # Field name made lowercase.
    parameter_type = models.CharField(db_column='PARAMETER_TYPE', max_length=100)  # Field name made lowercase.
    parameter_value = models.CharField(db_column='PARAMETER_VALUE', max_length=2500, blank=True, null=True)  # Field name made lowercase.
    identifying = models.CharField(db_column='IDENTIFYING', max_length=1)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BATCH_JOB_EXECUTION_PARAMS'


class BatchJobInstance(models.Model):
    job_instance_id = models.BigIntegerField(db_column='JOB_INSTANCE_ID', primary_key=True)  # Field name made lowercase.
    version = models.BigIntegerField(db_column='VERSION', blank=True, null=True)  # Field name made lowercase.
    job_name = models.CharField(db_column='JOB_NAME', max_length=100)  # Field name made lowercase.
    job_key = models.CharField(db_column='JOB_KEY', max_length=32)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BATCH_JOB_INSTANCE'
        unique_together = (('job_name', 'job_key'),)


class BatchStepExecution(models.Model):
    step_execution_id = models.BigIntegerField(db_column='STEP_EXECUTION_ID', primary_key=True)  # Field name made lowercase.
    version = models.BigIntegerField(db_column='VERSION')  # Field name made lowercase.
    step_name = models.CharField(db_column='STEP_NAME', max_length=100)  # Field name made lowercase.
    job_execution = models.ForeignKey(BatchJobExecution, models.DO_NOTHING, db_column='JOB_EXECUTION_ID')  # Field name made lowercase.
    create_time = models.DateTimeField(db_column='CREATE_TIME')  # Field name made lowercase.
    start_time = models.DateTimeField(db_column='START_TIME', blank=True, null=True)  # Field name made lowercase.
    end_time = models.DateTimeField(db_column='END_TIME', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    commit_count = models.BigIntegerField(db_column='COMMIT_COUNT', blank=True, null=True)  # Field name made lowercase.
    read_count = models.BigIntegerField(db_column='READ_COUNT', blank=True, null=True)  # Field name made lowercase.
    filter_count = models.BigIntegerField(db_column='FILTER_COUNT', blank=True, null=True)  # Field name made lowercase.
    write_count = models.BigIntegerField(db_column='WRITE_COUNT', blank=True, null=True)  # Field name made lowercase.
    read_skip_count = models.BigIntegerField(db_column='READ_SKIP_COUNT', blank=True, null=True)  # Field name made lowercase.
    write_skip_count = models.BigIntegerField(db_column='WRITE_SKIP_COUNT', blank=True, null=True)  # Field name made lowercase.
    process_skip_count = models.BigIntegerField(db_column='PROCESS_SKIP_COUNT', blank=True, null=True)  # Field name made lowercase.
    rollback_count = models.BigIntegerField(db_column='ROLLBACK_COUNT', blank=True, null=True)  # Field name made lowercase.
    exit_code = models.CharField(db_column='EXIT_CODE', max_length=2500, blank=True, null=True)  # Field name made lowercase.
    exit_message = models.CharField(db_column='EXIT_MESSAGE', max_length=2500, blank=True, null=True)  # Field name made lowercase.
    last_updated = models.DateTimeField(db_column='LAST_UPDATED', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BATCH_STEP_EXECUTION'


class BatchStepExecutionContext(models.Model):
    step_execution = models.OneToOneField(BatchStepExecution, models.DO_NOTHING, db_column='STEP_EXECUTION_ID', primary_key=True)  # Field name made lowercase.
    short_context = models.CharField(db_column='SHORT_CONTEXT', max_length=2500)  # Field name made lowercase.
    serialized_context = models.TextField(db_column='SERIALIZED_CONTEXT', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'BATCH_STEP_EXECUTION_CONTEXT'


class Dcinside(models.Model):
    id = models.BigAutoField(primary_key=True)
    create_dt = models.DateTimeField()
    update_dt = models.DateTimeField()
    _id = models.TextField(db_column='_id')  # Field renamed because it started with '_'.
    author = models.TextField()
    category = models.TextField()
    content = models.TextField()
    press = models.TextField()
    reg_date = models.TextField(blank=True, null=True)
    sns_id = models.TextField()
    status = models.TextField()
    title = models.TextField()
    url = models.TextField()

    class Meta:
        managed = False
        db_table = 'dcinside'


class DomainRaw(models.Model):
    id = models.BigAutoField(primary_key=True)
    create_dt = models.DateTimeField()
    update_dt = models.DateTimeField()
    contents = models.TextField()
    contents_dt = models.TextField()
    contents_raw = models.TextField()
    contents_writer = models.TextField()
    domain_code = models.TextField()
    title = models.TextField()

    class Meta:
        managed = False
        db_table = 'domain_raw'


class Instagram(models.Model):
    id = models.BigAutoField(primary_key=True)
    create_dt = models.DateTimeField()
    update_dt = models.DateTimeField()
    _id = models.TextField(db_column='_id')  # Field renamed because it started with '_'.
    author = models.TextField()
    category = models.TextField()
    content = models.TextField()
    press = models.TextField()
    reg_date = models.TextField()
    sns_id = models.TextField()
    status = models.TextField()
    title = models.TextField()
    url = models.TextField()

    class Meta:
        managed = False
        db_table = 'instagram'


class Twitter(models.Model):
    id = models.BigAutoField(primary_key=True)
    create_dt = models.DateTimeField()
    update_dt = models.DateTimeField()
    _id = models.TextField(db_column='_id')  # Field renamed because it started with '_'.
    author = models.TextField()
    category = models.TextField()
    content = models.TextField()
    press = models.TextField()
    reg_date = models.TextField()
    sns_id = models.TextField()
    status = models.TextField()
    title = models.TextField()
    url = models.TextField()

    class Meta:
        managed = False
        db_table = 'twitter'


class Youtube(models.Model):
    id = models.BigAutoField(primary_key=True)
    create_dt = models.DateTimeField()
    update_dt = models.DateTimeField()
    _id = models.TextField(db_column='_id')  # Field renamed because it started with '_'.
    author = models.TextField()
    category = models.TextField()
    content = models.TextField()
    press = models.TextField()
    reg_date = models.TextField()
    sns_id = models.TextField()
    status = models.TextField()
    title = models.TextField()
    url = models.TextField()

    class Meta:
        managed = False
        db_table = 'youtube'
