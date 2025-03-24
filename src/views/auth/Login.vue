<!-- 登录页面 -->
<!-- views/auth/Login.vue -->

<template>
  <div class="login-container">
    <h2 class="page-title">登录</h2>
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
      <n-form-item>
        <div class="form-options">
          <n-checkbox v-model:checked="formValue.rememberMe">记住我</n-checkbox>
          <n-button text @click="goToForgotPassword">忘记密码？</n-button>
        </div>
      </n-form-item>
      <n-form-item>
        <n-button
          type="primary"
          block
          :loading="loading"
          @click="handleSubmit"
        >
          登录
        </n-button>
      </n-form-item>
      <n-form-item>
        <div class="register-link">
          还没有账号？
          <n-button text @click="goToRegister">立即注册</n-button>
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
  NCheckbox,
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
  rememberMe: false
})

// 表单验证规则
const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

// 提交表单
const handleSubmit = (e) => {
  e.preventDefault()
  formRef.value?.validate(async (errors) => {
    if (!errors) {
      loading.value = true
      
      try {
        const result = await userStore.userLogin({
          username: formValue.username,
          password: formValue.password,
          rememberMe: formValue.rememberMe
        })
        
        if (result.success) {
          message.success('登录成功')
        }
      } catch (error) {
        console.error('登录失败:', error)
      } finally {
        loading.value = false
      }
    }
  })
}

// 跳转到注册页面
const goToRegister = () => {
  router.push({ name: 'Register' })
}

// 跳转到忘记密码页面
const goToForgotPassword = () => {
  router.push({ name: 'ForgotPassword' })
}
</script>

<style scoped>
.login-container {
  padding: 24px;
}

.page-title {
  text-align: center;
  margin-bottom: 24px;
  font-size: 24px;
  color: #333;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.register-link {
  text-align: center;
  margin-top: 16px;
  font-size: 14px;
  color: #666;
}
</style>
