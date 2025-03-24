<!-- 绑定原平台账号页面 -->
<!-- views/auth/BindAccount.vue -->

<template>
  <div class="bind-account-container">
    <h2 class="page-title">绑定原平台账号</h2>
    <div class="bind-description">
      <n-alert type="info" :show-icon="true">
        <template #icon>
          <n-icon><information-circle-outline /></n-icon>
        </template>
        <p>请绑定您的原平台账号，以便我们为您提供更好的服务。</p>
        <p>绑定后，您可以查看您在原平台的所有考试成绩和分析数据。</p>
      </n-alert>
    </div>
    <n-form
      ref="formRef"
      :model="formValue"
      :rules="rules"
      label-placement="left"
      label-width="auto"
      require-mark-placement="right-hanging"
      size="medium"
      :show-feedback="true"
      :show-label="true"
    >
      <n-form-item path="loginName" label="原平台账号">
        <n-input
          v-model:value="formValue.loginName"
          placeholder="请输入原平台账号"
          @keydown.enter="handleSubmit"
        />
      </n-form-item>
      <n-form-item path="password" label="原平台密码">
        <n-input
          v-model:value="formValue.password"
          type="password"
          placeholder="请输入原平台密码"
          show-password-on="click"
          @keydown.enter="handleSubmit"
        />
      </n-form-item>
      <n-form-item>
        <n-button
          type="primary"
          block
          :loading="loading"
          @click="handleSubmit"
        >
          绑定账号
        </n-button>
      </n-form-item>
      <n-form-item>
        <div class="skip-link">
          <n-button text @click="skipBinding">暂不绑定，稍后再说</n-button>
        </div>
      </n-form-item>
    </n-form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { 
  NForm, 
  NFormItem, 
  NInput, 
  NButton,
  NAlert,
  NIcon,
  useMessage
} from 'naive-ui'
import { InformationCircleOutline } from '@vicons/ionicons5'

// 路由实例
const router = useRouter()

// 用户状态
const userStore = useUserStore()

// 消息提示
const message = useMessage()

// 表单引用
const formRef = ref(null)

// 加载状态
const loading = ref(false)

// 表单数据
const formValue = reactive({
  loginName: '',
  password: ''
})

// 表单验证规则
const rules = {
  loginName: [
    { required: true, message: '请输入原平台账号', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入原平台密码', trigger: 'blur' }
  ]
}

// 提交表单
const handleSubmit = (e) => {
  e.preventDefault()
  formRef.value?.validate(async (errors) => {
    if (!errors) {
      loading.value = true
      
      try {
        const result = await userStore.bindAccount({
          loginName: formValue.loginName,
          password: formValue.password,
          deviceType: 1,
          roleType: 1
        })
        
        if (result.success) {
          message.success('账号绑定成功')
          router.push({ name: 'Dashboard' })
        }
      } catch (error) {
        console.error('绑定失败:', error)
      } finally {
        loading.value = false
      }
    }
  })
}

// 跳过绑定
const skipBinding = () => {
  message.info('您可以稍后在个人设置中绑定原平台账号')
  router.push({ name: 'Dashboard' })
}
</script>

<style scoped>
.bind-account-container {
  padding: 24px;
}

.page-title {
  text-align: center;
  margin-bottom: 24px;
  font-size: 24px;
  color: #333;
}

.bind-description {
  margin-bottom: 24px;
}

.skip-link {
  text-align: center;
  margin-top: 16px;
  font-size: 14px;
  color: #666;
}
</style>
