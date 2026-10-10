export interface PatientProfile {
  id: string
  username: string
  name: string
  birthday: string | null
  phone: string | null
  gender: string | null
}

interface LoginResponse {
  code: number
  message: string
  data: PatientProfile | null
}

export async function loginPatient(username: string, password: string): Promise<PatientProfile> {
  const response = await fetch('/api/patients/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password }),
  })

  if (!response.ok) {
    throw new Error(`登录请求失败: ${response.status}`)
  }

  const body = (await response.json()) as LoginResponse
  if (body.code !== 0 || !body.data) {
    throw new Error(body.message || '用户名或密码错误')
  }

  return body.data
}
