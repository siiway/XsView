<!-- 注册页面 -->
<!-- views/auth/Register.vue -->

<template>
  <div class="register-container">
    <h2 class="page-title">注册</h2>
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
      <n-form-item path="username" label="用户名">
        <n-input
          v-model:value="formValue.username"
          placeholder="请输入用户名"
          @keydown.enter="handleSubmit"
        />
      </n-form-item>
      <n-form-item path="password" label="密码">
        <n-input
          v-model:value="formValue.password"
          type="password"
          placeholder="请输入密码"
          show-password-on="click"
          @keydown.enter="handleSubmit"
        />
      </n-form-item>
      <n-form-item path="confirmPassword" label="确认密码">
        <n-input
          v-model:value="formValue.confirmPassword"
          type="password"
          placeholder="请再次输入密码"
          show-password-on="click"
          @keydown.enter="handleSubmit"
        />
      </n-form-item>
      <n-form-item path="email" label="邮箱">
        <n-input
          v-model:value="formValue.email"
          placeholder="请输入邮箱"
          @keydown.enter="handleSubmit"
        />
      </n-form-item>
      <n-form-item path="phone" label="手机号">
        <n-input
          v-model:value="formValue.phone"
          placeholder="请输入手机号"
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
          注册
        </n-button>
      </n-form-item>
      <n-form-item>
        <div class="login-link">
          已有账号？
          <n-button text @click="goToLogin">立即登录</n-button>
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
  useMessage
} from 'naive-ui'

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
  username: '',
  password: '',
  confirmPassword: '',
  email: '',
  phone: ''
})

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应在3-20个字符之间', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    {
      validator: (rule, value) => {
        return value === formValue.password
      },
      message: '两次输入的密码不一致',
      trigger: 'blur'
    }
  ],
  email: [
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号码', trigger: 'blur' }
  ]
}

// 提交表单
const handleSubmit = (e) => {
  e.preventDefault()
  formRef.value?.validate(async (errors) => {
    if (!errors) {
      loading.value = true
      
      try {
        const result = await userStore.userRegister({
          username: formValue.username,
          password: formValue.password,
          email: formValue.email,
          phone: formValue.phone
        })
        
        if (result.success) {
          message.success('注册成功，请绑定原平台账号')
        }
      } catch (error) {
        console.error('注册失败:', error)
      } finally {
        loading.value = false
      }
    }
  })
}

// 跳转到登录页面
const goToLogin = () => {
  router.push({ name: 'Login' })
}
</script>

<style scoped>
.register-container {
  padding: 24px;
}

.page-title {
  text-align: center;
  margin-bottom: 24px;
  font-size: 24px;
  color: #333;
}

.login-link {
  text-align: center;
  margin-top: 16px;
  font-size: 14px;
  color: #666;
}
</style>
