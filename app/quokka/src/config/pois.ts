export interface Poi {
  id: number
  name: string
  location: {
    lat: number
    lon: number
  }
  lat: number
  lon: number
  description: string | null
  opening_hours: string | null
  category: string | null
  sub_category: string | null
  url: string | null
  website: string | null
  image: string | null
}
