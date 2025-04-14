import { defineStore } from 'pinia'
import * as userApi from '@/api/user' // 确保 api/user.js 中有所有需要的函数
import { ElMessage } from 'element-plus'

// 假设 api/user.js 导出了一个 getMe 函数用于请求 /users/me/
// 并且 login 函数返回的数据包含 userInfo (含 userType) 或需要调用 getMe 获取

export const useUserStore = defineStore('user', {
  // 从 localStorage 初始化 state
  state: () => ({
    token: localStorage.getItem('userToken') || '',
    // userInfo 现在也包含 userType
    userInfo: (() => {
        try {
            const info = JSON.parse(localStorage.getItem('userInfo')) || null;
            // 确保 userInfo 至少是个对象，方便后续访问
            return info ? info : {};
        } catch (e) {
            console.error("无法解析 localStorage 中的 userInfo:", e);
            localStorage.removeItem('userInfo'); // 清除无效数据
            return {}; // 返回空对象
        }
    })(),
    // isLoggedIn 状态应基于 token 和 userInfo.id 是否存在
    isLoggedIn: !!localStorage.getItem('userToken') && !!JSON.parse(localStorage.getItem('userInfo') || '{}').id,
  }),

  getters: {
    // Getter 现在直接返回 state 的值
    username: (state) => state.userInfo?.username || '',
    avatar: (state) => state.userInfo?.avatar || '',
    userId: (state) => state.userInfo?.id || null,
    // 新增：获取用户类型
    userType: (state) => state.userInfo?.user_type || null, // 假设后端返回的字段是 user_type

    // 可以添加更具体的类型检查 getter
    isPoorUser: (state) => state.userInfo?.user_type === 'poor',
    isSocialUser: (state) => state.userInfo?.user_type === 'social',
    isAdminUser: (state) => state.userInfo?.user_type === 'admin',
  },

  actions: {
    // 设置 Token 并存入 localStorage
    setToken(token) {
      this.token = token;
      if (token) {
        localStorage.setItem('userToken', token);
      } else {
        localStorage.removeItem('userToken');
      }
    },

    // 设置用户信息并存入 localStorage
    setUserInfo(userInfo) {
      if (userInfo && userInfo.id) { // 确保用户信息有效（至少有id）
        this.userInfo = userInfo;
        localStorage.setItem('userInfo', JSON.stringify(userInfo));
        this.isLoggedIn = true; // 获取到有效用户信息，表示已登录
      } else {
        this.userInfo = {}; // 清空用户信息
        localStorage.removeItem('userInfo');
        this.isLoggedIn = false; // 清除用户信息，表示未登录
      }
    },

    async login(credentials) {
      try {
        const loginData = await userApi.login(credentials); // 调用登录 API
        // 假设 loginData 包含 access token 和 user 信息 (包括 user_type)
        // 或者只包含 token，然后需要调用 fetchUserInfo
        if (loginData.access) {
          this.setToken(loginData.access);

          this.setUserInfo(loginData.user)

          if (this.isLoggedIn) { // 确认用户信息获取成功
             ElMessage.success('登录成功');
             return true;
          } else {
             ElMessage.error('登录成功，但获取用户信息失败');
             // fetchUserInfo 失败时内部已调用 logout 清理状态
             return false;
          }
        } else {
          throw new Error("登录响应中缺少 token");
        }
      } catch (error) {
        console.error('登录失败:', error);
        await this.logout(); // 登录失败时确保状态被清除
        ElMessage.error(error.message || '登录失败，请检查用户名或密码');
        return false;
      }
    },

    async register(userData) {
      // 注册逻辑保持不变，注册后通常需要用户手动登录
      try {
        await userApi.register(userData); // 调用注册 API
        ElMessage.success('注册成功，请登录');
        return true;
      } catch (error) {
        console.error('注册失败:', error);
        ElMessage.error(error.response?.data?.detail || error.message || '注册失败');
        return false;
      }
    },

    // 获取用户信息 (通常在登录后或页面刷新时调用)
    async fetchUserInfo() {
      if (!this.token) {
          console.warn("没有 token，无法获取用户信息。");
          // 不需要在这里 logout，因为可能是页面加载时无 token 的正常情况
          this.setUserInfo(null); // 确保状态被清理
          return;
      }
      try {
        console.log("尝试从 /users/me/ 获取用户信息...");
        const userInfoData = await userApi.getMe(); // 调用 getMe API
        console.log("获取到的用户信息:", userInfoData);
        if (userInfoData && userInfoData.id) {
            this.setUserInfo(userInfoData); // 设置用户信息, 包括 userType
        } else {
            throw new Error("从 /users/me/ 获取的用户信息无效或不包含 ID");
        }
      } catch (error) {
        console.error('获取用户信息失败:', error);
        await this.logout(); // 获取失败时，清除登录状态
      }
    },

    // 更新用户信息
    async updateUserInfo(userData) {
      // ... (基本不变, 确保更新后也保存 userType) ...
      const userId = this.userId;
      if (!userId) {
        ElMessage.error('无法更新信息：用户未登录或用户信息不完整');
        return false;
      }
      try {
        const updatedUserInfo = await userApi.updateUserInfo(userId, userData);
        // 合并旧信息和更新后的信息，确保 userType 等字段保留
        this.setUserInfo({ ...this.userInfo, ...updatedUserInfo });
        ElMessage.success('用户信息更新成功');
        return true;
      } catch (error) {
        console.error('更新用户信息失败:', error);
        ElMessage.error(error.response?.data?.detail || error.message || '更新用户信息失败');
        return false;
      }
    },

    // 修改密码
    async changePassword(passwordData) {
      // ... (保持不变) ...
       const userId = this.userId;
       if (!userId) {
         ElMessage.error('无法修改密码：用户未登录');
         return false;
       }
      try {
        await userApi.changePassword(passwordData);
        ElMessage.success('密码修改成功');
        return true;
      } catch (error) {
        console.error('密码修改失败:', error);
        ElMessage.error(error.response?.data?.detail || error.message || '密码修改失败');
        return false;
      }
    },

    // 退出登录
    async logout() {
      try {
        if (userApi.logout) {
            await userApi.logout();
        }
      } catch(error) {
        console.error('调用后端登出接口失败 (不影响前端状态清理):', error);
      } finally {
        // 清理 token 和 userInfo
        this.setToken(null);
        this.setUserInfo(null); // 会自动设置 isLoggedIn 为 false
        console.log("用户已登出，状态已清理。");
      }
    }
  }
})
