export interface DoctorItem {
  id: string
  username: string
  name: string
  title: string
  department: string
  avatar: string
  experience: string
  specialties: string[]
  isActive: boolean
}

interface DoctorListResponse {
  code: number
  message: string
  data: DoctorItem[]
}

export async function fetchDoctors(): Promise<DoctorItem[]> {
  const response = await fetch('/api/doctors')
  if (!response.ok) {
    throw new Error(`获取医生列表失败: ${response.status}`)
  }

  const body = (await response.json()) as DoctorListResponse
  if (body.code !== 0) {
    throw new Error(body.message || '获取医生列表失败')
  }

  return body.data
}
