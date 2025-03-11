from django.db import models
from django.contrib.auth.models import AbstractUser

# 用户模型 (继承 Django 默认 User 模型，可以根据需要扩展)
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('poor_household', '贫困户'),
        ('admin', '管理员'),
        ('company', '社会公司'),
        ('volunteer', '志愿者'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='poor_household', verbose_name='用户类型')

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="backend_user_groups",  # 添加 related_name
        related_query_name="backend_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="backend_user_permissions", # 添加 related_name
        related_query_name="backend_user",
    )

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


# 贫困户信息模型
class PoorHousehold(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, verbose_name='用户') # 与用户模型一对一关联
    name = models.CharField(max_length=50, verbose_name='姓名')
    id_card = models.CharField(max_length=20, verbose_name='身份证号')
    phone_number = models.CharField(max_length=20, verbose_name='联系方式')
    address = models.TextField(verbose_name='家庭住址')
    family_size = models.IntegerField(verbose_name='家庭人口')
    poverty_type = models.CharField(max_length=50, verbose_name='贫困类型') # 例如：因病、因残、因学等
    application_materials = models.TextField(blank=True, null=True, verbose_name='申请材料') # 可以存储文件路径或链接
    application_status = models.CharField(max_length=20, default='待审核', verbose_name='申请状态') # 例如：待审核、审核通过、审核不通过

    class Meta:
        verbose_name = '贫困户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 贫困户审核记录模型
class AuditRecord(models.Model):
    poor_household = models.ForeignKey(PoorHousehold, on_delete=models.CASCADE, verbose_name='贫困户')
    auditor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='审核人') # 管理员用户
    audit_time = models.DateTimeField(auto_now_add=True, verbose_name='审核时间')
    audit_result = models.BooleanField(verbose_name='审核结果') # True: 通过, False: 不通过
    audit_opinion = models.TextField(blank=True, null=True, verbose_name='审核意见')

    class Meta:
        verbose_name = '贫困户审核记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.poor_household.name} - {self.audit_result}"

# 帮扶对接模型
class AssistanceConnection(models.Model):
    poor_household = models.ForeignKey(PoorHousehold, on_delete=models.CASCADE, verbose_name='贫困户')
    assistance_type = models.CharField(max_length=50, verbose_name='帮扶类型') # 例如：寒暑假辅导、技能培训
    assistance_provider = models.CharField(max_length=100, verbose_name='帮扶提供方') # 可以是社会公司或志愿者名称
    assistance_content = models.TextField(verbose_name='帮扶内容')
    assistance_time = models.DateField(verbose_name='帮扶时间')
    assistance_status = models.CharField(max_length=20, default='待对接', verbose_name='帮扶状态') # 例如：待对接、已对接、已完成

    class Meta:
        verbose_name = '帮扶对接信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.poor_household.name} - {self.assistance_type}"

# 物资援助模型
class MaterialAssistance(models.Model):
    poor_household = models.ForeignKey(PoorHousehold, on_delete=models.CASCADE, verbose_name='贫困户')
    donor = models.CharField(max_length=100, verbose_name='捐赠方') # 例如：政府、社会组织名称
    material_type = models.CharField(max_length=50, verbose_name='物资类型') # 例如：米、面、粮油
    material_quantity = models.CharField(max_length=50, verbose_name='物资数量') # 例如：10kg 大米
    assistance_time = models.DateField(verbose_name='援助时间')
    assistance_status = models.CharField(max_length=20, default='待发放', verbose_name='发放状态') # 例如：待发放、已发放

    class Meta:
        verbose_name = '物资援助信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.poor_household.name} - {self.material_type}"

# 教育资助模型
class EducationAssistance(models.Model):
    poor_household = models.ForeignKey(PoorHousehold, on_delete=models.CASCADE, verbose_name='贫困户')
    sponsor = models.CharField(max_length=100, verbose_name='资助方') # 例如：慈善机构、个人
    assistance_type = models.CharField(max_length=50, verbose_name='资助类型') # 例如：学费减免、全额资助
    assistance_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='资助金额')
    academic_year = models.CharField(max_length=20, verbose_name='资助学年') # 例如：2023-2024学年
    assistance_status = models.CharField(max_length=20, default='待资助', verbose_name='资助状态') # 例如：待资助、已资助

    class Meta:
        verbose_name = '教育资助信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.poor_household.name} - {self.assistance_type}"

# 商品模型
class Product(models.Model):
    poor_household = models.ForeignKey(PoorHousehold, on_delete=models.CASCADE, verbose_name='贫困户') # 上传商品的贫困户
    product_name = models.CharField(max_length=100, verbose_name='商品名称')
    product_image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='商品图片') # 图片上传路径
    product_description = models.TextField(verbose_name='商品描述')
    product_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    product_stock = models.IntegerField(default=0, verbose_name='商品库存')
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')

    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.product_name

# 订单模型
class Order(models.Model):
    order_id = models.CharField(max_length=50, unique=True, verbose_name='订单号') # 可以自定义生成订单号
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='买家') # 下单用户
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    quantity = models.IntegerField(verbose_name='购买数量')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单总价')
    order_time = models.DateTimeField(auto_now_add=True, verbose_name='下单时间')
    payment_status = models.CharField(max_length=20, default='待支付', verbose_name='支付状态') # 例如：待支付、已支付、已退款
    payment_method = models.CharField(max_length=50, verbose_name='支付方式') # 例如：支付宝、微信、银行卡
    delivery_status = models.CharField(max_length=20, default='待发货', verbose_name='发货状态') # 例如：待发货、已发货、已收货
    tracking_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='物流单号') # 可选

    class Meta:
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_id

# 物流跟踪模型
class Logistics(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key=True, verbose_name='订单') # 与订单模型一对一关联
    logistics_company = models.CharField(max_length=100, verbose_name='物流公司')
    tracking_number = models.CharField(max_length=50, verbose_name='物流单号')
    logistics_status = models.CharField(max_length=50, verbose_name='物流状态') # 例如：运输中、已签收，可以对接物流API实时更新
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '物流信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tracking_number

# 客服消息模型
class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name='发送者')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', verbose_name='接收者')
    message_content = models.TextField(verbose_name='消息内容')
    send_time = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')

    class Meta:
        verbose_name = '客服消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.send_time}"