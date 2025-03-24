<!-- 后台管理系统用户管理页面 -->
<!-- frontend/scorex-admin/src/views/user/UserManagement.vue -->

<template>
  <div class="user-management-container">
    <!-- 搜索和操作栏 -->
    <a-card class="search-card">
      <a-row :gutter="16">
        <a-col :span="6" :xs="24" :sm="12" :md="8" :lg="6">
          <a-input
            v-model="searchForm.keyword"
            placeholder="搜索用户名/手机号"
            allow-clear
          >
            <template #prefix>
              <icon-search />
            </template>
          </a-input>
        </a-col>
        <a-col :span="6" :xs="24" :sm="12" :md="8" :lg="6">
          <a-select
            v-model="searchForm.role"
            placeholder="角色"
            allow-clear
            style="width: 100%"
          >
            <a-option v-for="role in roleOptions" :key="role.value" :value="role.value">
              {{ role.label }}
            </a-option>
          </a-select>
        </a-col>
        <a-col :span="6" :xs="24" :sm="12" :md="8" :lg="6">
          <a-select
            v-model="searchForm.status"
            placeholder="状态"
            allow-clear
            style="width: 100%"
          >
            <a-option v-for="status in statusOptions" :key="status.value" :value="status.value">
              {{ status.label }}
            </a-option>
          </a-select>
        </a-col>
        <a-col :span="6" :xs="24" :sm="12" :md="8" :lg="6">
          <a-space>
            <a-button type="primary" @click="handleSearch">
              <template #icon>
                <icon-search />
              </template>
              搜索
            </a-button>
            <a-button @click="resetSearch">
              <template #icon>
                <icon-refresh />
              </template>
              重置
            </a-button>
          </a-space>
        </a-col>
      </a-row>
    </a-card>

    <!-- 用户列表 -->
    <a-card class="table-card">
      <template #title>
        用户列表
      </template>
      <template #extra>
        <a-space>
          <a-button type="primary" @click="openAddUserModal">
            <template #icon>
              <icon-plus />
            </template>
            新增用户
          </a-button>
          <a-button @click="handleBatchExport">
            <template #icon>
              <icon-download />
            </template>
            导出
          </a-button>
        </a-space>
      </template>

      <a-table
        :loading="loading"
        :columns="columns"
        :data="userData"
        :pagination="pagination"
        @page-change="onPageChange"
        @page-size-change="onPageSizeChange"
        row-key="id"
      >
        <template #avatar="{ record }">
          <a-avatar :style="{ backgroundColor: getAvatarColor(record.name) }">
            {{ record.name.charAt(0).toUpperCase() }}
          </a-avatar>
        </template>
        
        <template #role="{ record }">
          <a-tag :color="getRoleColor(record.role)">{{ record.role }}</a-tag>
        </template>
        
        <template #status="{ record }">
          <a-badge
            :status="record.status === '正常' ? 'success' : (record.status === '禁用' ? 'error' : 'warning')"
            :text="record.status"
          />
        </template>
        
        <template #operations="{ record }">
          <a-space>
            <a-button type="text" size="small" @click="handleEdit(record)">
              编辑
            </a-button>
            <a-divider direction="vertical" />
            <a-button type="text" size="small" @click="handleResetPassword(record)">
              重置密码
            </a-button>
            <a-divider direction="vertical" />
            <a-button
              type="text"
              size="small"
              :status="record.status === '正常' ? 'danger' : 'success'"
              @click="handleToggleStatus(record)"
            >
              {{ record.status === '正常' ? '禁用' : '启用' }}
            </a-button>
          </a-space>
        </template>
      </a-table>
    </a-card>

    <!-- 新增/编辑用户弹窗 -->
    <a-modal
      v-model:visible="userModalVisible"
      :title="isEdit ? '编辑用户' : '新增用户'"
      @cancel="closeUserModal"
      @before-ok="handleSubmitUser"
    >
      <a-form :model="userForm" ref="userFormRef" :rules="userFormRules" label-align="right" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }">
        <a-form-item field="name" label="用户名" required>
          <a-input v-model="userForm.name" placeholder="请输入用户名" />
        </a-form-item>
        <a-form-item field="phone" label="手机号" required>
          <a-input v-model="userForm.phone" placeholder="请输入手机号" />
        </a-form-item>
        <a-form-item field="email" label="邮箱">
          <a-input v-model="userForm.email" placeholder="请输入邮箱" />
        </a-form-item>
        <a-form-item field="role" label="角色" required>
          <a-select v-model="userForm.role" placeholder="请选择角色">
            <a-option v-for="role in roleOptions" :key="role.value" :value="role.value">
              {{ role.label }}
            </a-option>
          </a-select>
        </a-form-item>
        <a-form-item field="status" label="状态" required>
          <a-select v-model="userForm.status" placeholder="请选择状态">
            <a-option v-for="status in statusOptions" :key="status.value" :value="status.value">
              {{ status.label }}
            </a-option>
          </a-select>
        </a-form-item>
        <a-form-item v-if="!isEdit" field="password" label="密码" required>
          <a-input-password v-model="userForm.password" placeholder="请输入密码" />
        </a-form-item>
        <a-form-item v-if="!isEdit" field="confirmPassword" label="确认密码" required>
          <a-input-password v-model="userForm.confirmPassword" placeholder="请再次输入密码" />
        </a-form-item>
        <a-form-item field="remark" label="备注">
          <a-textarea v-model="userForm.remark" placeholder="请输入备注信息" />
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 重置密码弹窗 -->
    <a-modal
      v-model:visible="resetPasswordVisible"
      title="重置密码"
      @cancel="closeResetPasswordModal"
      @before-ok="handleConfirmResetPassword"
    >
      <a-form :model="resetPasswordForm" ref="resetPasswordFormRef" :rules="resetPasswordRules" label-align="right" :label-col-props="{ span: 6 }" :wrapper-col-props="{ span: 18 }">
        <a-form-item field="newPassword" label="新密码" required>
          <a-input-password v-model="resetPasswordForm.newPassword" placeholder="请输入新密码" />
        </a-form-item>
        <a-form-item field="confirmPassword" label="确认密码" required>
          <a-input-password v-model="resetPasswordForm.confirmPassword" placeholder="请再次输入新密码" />
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue';
import { Message } from '@arco-design/web-vue';

export default {
  setup() {
    // 搜索表单
    const searchForm = reactive({
      keyword: '',
      role: undefined,
      status: undefined
    });

    // 用户表单
    const userForm = reactive({
      id: '',
      name: '',
      phone: '',
      email: '',
      role: '',
      status: '正常',
      password: '',
      confirmPassword: '',
      remark: ''
    });

    // 重置密码表单
    const resetPasswordForm = reactive({
      userId: '',
      newPassword: '',
      confirmPassword: ''
    });

    // 表单引用
    const userFormRef = ref(null);
    const resetPasswordFormRef = ref(null);

    // 状态变量
    const loading = ref(false);
    const userModalVisible = ref(false);
    const resetPasswordVisible = ref(false);
    const isEdit = ref(false);
    const currentUserId = ref('');

    // 分页配置
    const pagination = reactive({
      current: 1,
      pageSize: 10,
      total: 0,
      showTotal: true,
      showPageSize: true,
      pageSizeOptions: [10, 20, 50, 100]
    });

    // 角色选项
    const roleOptions = [
      { label: '管理员', value: '管理员' },
      { label: '教师', value: '教师' },
      { label: '学生', value: '学生' },
      { label: '家长', value: '家长' }
    ];

    // 状态选项
    const statusOptions = [
      { label: '正常', value: '正常' },
      { label: '禁用', value: '禁用' },
      { label: '待激活', value: '待激活' }
    ];

    // 表格列定义
    const columns = [
      {
        title: '头像',
        slotName: 'avatar',
        width: 80,
        align: 'center'
      },
      {
        title: '用户名',
        dataIndex: 'name'
      },
      {
        title: '手机号',
        dataIndex: 'phone'
      },
      {
        title: '邮箱',
        dataIndex: 'email'
      },
      {
        title: '角色',
        slotName: 'role'
      },
      {
        title: '状态',
        slotName: 'status'
      },
      {
        title: '注册时间',
        dataIndex: 'registerTime'
      },
      {
        title: '最后登录',
        dataIndex: 'lastLoginTime'
      },
      {
        title: '操作',
        slotName: 'operations',
        fixed: 'right',
        width: 200
      }
    ];

    // 用户表单校验规则
    const userFormRules = {
      name: [
        { required: true, message: '请输入用户名' },
        { minLength: 2, message: '用户名至少2个字符' }
      ],
      phone: [
        { required: true, message: '请输入手机号' },
        { match: /^1[3-9]\d{9}$/, message: '请输入正确的手机号' }
      ],
      email: [
        { type: 'email', message: '请输入正确的邮箱地址' }
      ],
      role: [
        { required: true, message: '请选择角色' }
      ],
      status: [
        { required: true, message: '请选择状态' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: ['change', 'blur'] },
        { minLength: 6, message: '密码至少6个字符' }
      ],
      confirmPassword: [
        { required: true, message: '请确认密码', trigger: ['change', 'blur'] },
        {
          validator: (value, cb) => {
            if (value !== userForm.password) {
              return cb('两次输入的密码不一致');
            }
            return cb();
          }
        }
      ]
    };

    // 重置密码表单校验规则
    const resetPasswordRules = {
      newPassword: [
        { required: true, message: '请输入新密码' },
        { minLength: 6, message: '密码至少6个字符' }
      ],
      confirmPassword: [
        { required: true, message: '请确认新密码' },
        {
          validator: (value, cb) => {
            if (value !== resetPasswordForm.newPassword) {
              return cb('两次输入的密码不一致');
            }
            return cb();
          }
        }
      ]
    };

    // 模拟用户数据
    const userData = ref([]);

    // 生命周期钩子
    onMounted(() => {
      fetchUserData();
    });

    // 获取用户数据
    const fetchUserData = () => {
      loading.value = true;
      
      // 模拟API请求
      setTimeout(() => {
        // 生成模拟数据
        const mockData = generateMockUserData();
        userData.value = mockData.list;
        pagination.total = mockData.total;
        loading.value = false;
      }, 800);
    };

    // 生成模拟用户数据
    const generateMockUserData = () => {
      const roles = ['管理员', '教师', '学生', '家长'];
      const statuses = ['正常', '禁用', '待激活'];
      const names = ['张三', '李四', '王五', '赵六', '钱七', '孙八', '周九', '吴十'];
      
      const mockList = [];
      const totalItems = 58;
      
      for (let i = 1; i <= totalItems; i++) {
        const name = names[Math.floor(Math.random() * names.length)] + i;
        const role = roles[Math.floor(Math.random() * roles.length)];
        const status = statuses[Math.floor(Math.random() * statuses.length)];
        
        const user = {
          id: `user-${i}`,
          name,
          phone: `1${Math.floor(Math.random() * 9) + 3}${Math.floor(Math.random() * 10000000).toString().padStart(8, '0')}`,
          email: `${name.toLowerCase()}@example.com`,
          role,
          status,
          registerTime: `2025-0${Math.floor(Math.random() * 3) + 1}-${Math.floor(Math.random() * 28) + 1}`,
          lastLoginTime: `2025-03-${Math.floor(Math.random() * 24) + 1} ${Math.floor(Math.random() * 24).toString().padStart(2, '0')}:${Math.floor(Math.random() * 60).toString().padStart(2, '0')}`,
          remark: `这是${name}的账号备注信息`
        };
        
        // 应用筛选条件
        let match = true;
        
        if (searchForm.keyword) {
          const keyword = searchForm.keyword.toLowerCase();
          const nameMatch = user.name.toLowerCase().includes(keyword);
          const phoneMatch = user.phone.includes(keyword);
          
          if (!nameMatch && !phoneMatch) {
            match = false;
          }
        }
        
        if (searchForm.role && user.role !== searchForm.role) {
          match = false;
        }
        
        if (searchForm.status && user.status !== searchForm.status) {
          match = false;
        }
        
        if (match) {
          mockList.push(user);
        }
      }
      
      // 分页
      const startIndex = (pagination.current - 1) * pagination.pageSize;
      const endIndex = startIndex + pagination.pageSize;
      const paginatedList = mockList.slice(startIndex, endIndex);
      
      return {
        list: paginatedList,
        total: mockList.length
      };
    };

    // 处理搜索
    const handleSearch = () => {
      pagination.current = 1;
      fetchUserData();
    };

    // 重置搜索
    const resetSearch = () => {
      searchForm.keyword = '';
      searchForm.role = undefined;
      searchForm.status = undefined;
      pagination.current = 1;
      fetchUserData();
    };

    // 处理分页变化
    const onPageChange = (page) => {
      pagination.current = page;
      fetchUserData();
    };

    // 处理每页条数变化
    const onPageSizeChange = (pageSize) => {
      pagination.pageSize = pageSize;
      pagination.current = 1;
      fetchUserData();
    };

    // 打开新增用户弹窗
    const openAddUserModal = () => {
      isEdit.value = false;
      resetUserForm();
      userModalVisible.value = true;
    };

    // 处理编辑用户
    const handleEdit = (record) => {
      isEdit.value = true;
      currentUserId.value = record.id;
      
      // 填充表单数据
      userForm.id = record.id;
      userForm.name = record.name;
      userForm.phone = record.phone;
      userForm.email = record.email;
      userForm.role = record.role;
      userForm.status = record.status;
      userForm.remark = record.remark;
      
      userModalVisible.value = true;
    };

    // 处理重置密码
    const handleResetPassword = (record) => {
      resetPasswordForm.userId = record.id;
      resetPasswordForm.newPassword = '';
      resetPasswordForm.confirmPassword = '';
      resetPasswordVisible.value = true;
    };

    // 处理切换用户状态
    const handleToggleStatus = (record) => {
      const newStatus = record.status === '正常' ? '禁用' : '正常';
      const action = newStatus === '正常' ? '启用' : '禁用';
      
      Message.success(`已${action}用户 ${record.name}`);
      
      // 在实际应用中，这里应该调用API来更新用户状态
      // 然后重新获取用户列表
      
      // 模拟更新
      const index = userData.value.findIndex(user => user.id === record.id);
      if (index !== -1) {
        userData.value[index].status = newStatus;
      }
    };

    // 处理批量导出
    const handleBatchExport = () => {
      Message.success('用户数据导出成功');
    };

    // 提交用户表单
    const handleSubmitUser = async (done) => {
      try {
        await userFormRef.value.validate();
        
        if (isEdit.value) {
          Message.success(`用户 ${userForm.name} 更新成功`);
        } else {
          Message.success(`用户 ${userForm.name} 创建成功`);
        }
        
        // 在实际应用中，这里应该调用API来创建或更新用户
        // 然后重新获取用户列表
        
        closeUserModal();
        fetchUserData();
        done();
      } catch (error) {
        done(false);
      }
    };

    // 确认重置密码
    const handleConfirmResetPassword = async (done) => {
      try {
        await resetPasswordFormRef.value.validate();
        
        Message.success('密码重置成功');
        
        // 在实际应用中，这里应该调用API来重置用户密码
        
        closeResetPasswordModal();
        done();
      } catch (error) {
        done(false);
      }
    };

    // 关闭用户弹窗
    const closeUserModal = () => {
      userModalVisible.value = false;
      resetUserForm();
    };

    // 关闭重置密码弹窗
    const closeResetPasswordModal = () => {
      resetPasswordVisible.value = false;
      resetPasswordForm.userId = '';
      resetPasswordForm.newPassword = '';
      resetPasswordForm.confirmPassword = '';
    };

    // 重置用户表单
    const resetUserForm = () => {
      userForm.id = '';
      userForm.name = '';
      userForm.phone = '';
      userForm.email = '';
      userForm.role = '';
      userForm.status = '正常';
      userForm.password = '';
      userForm.confirmPassword = '';
      userForm.remark = '';
    };

    // 获取头像颜色
    const getAvatarColor = (name) => {
      const colors = ['#165DFF', '#37C2FF', '#00B42A', '#FFAB00', '#FF7D00', '#EB0AA4', '#7816FF', '#86909C'];
      const index = name.charCodeAt(0) % colors.length;
      return colors[index];
    };

    // 获取角色颜色
    const getRoleColor = (role) => {
      const colorMap = {
        '管理员': 'blue',
        '教师': 'green',
        '学生': 'orange',
        '家长': 'purple'
      };
      return colorMap[role] || 'gray';
    };

    return {
      searchForm,
      userForm,
      resetPasswordForm,
      userFormRef,
      resetPasswordFormRef,
      loading,
      userModalVisible,
      resetPasswordVisible,
      isEdit,
      pagination,
      roleOptions,
      statusOptions,
      columns,
      userFormRules,
      resetPasswordRules,
      userData,
      handleSearch,
      resetSearch,
      onPageChange,
      onPageSizeChange,
      openAddUserModal,
      handleEdit,
      handleResetPassword,
      handleToggleStatus,
      handleBatchExport,
      handleSubmitUser,
      handleConfirmResetPassword,
      closeUserModal,
      closeResetPasswordModal,
      getAvatarColor,
      getRoleColor
    };
  }
};
</script>

<style scoped>
.user-management-container {
  padding: 16px;
}

.search-card {
  margin-bottom: 16px;
}

.table-card {
  margin-bottom: 16px;
}

@media (max-width: 768px) {
  .search-card .arco-col {
    margin-bottom: 16px;
  }
}
</style>
