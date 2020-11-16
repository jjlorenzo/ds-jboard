import { DateTime } from "luxon"
import { InjectionKey } from "vue"
import { Store } from "vuex"
import { createStore } from "vuex"
import { useStore as useStoreBase } from "vuex"
import { FetchError } from "./errors"

export const key: InjectionKey<Store<State>> = Symbol()

export const store = createStore<State>({
  actions: {
    backend({ commit, dispatch, getters: { description, location } }, backend) {
      commit("backend", backend)
      return dispatch("list", { description, location, page: 1 })
    },
    description({ commit, dispatch, getters: { location } }, description) {
      commit("description", description)
      return dispatch("list", { description, location, page: 1 })
    },
    descriptions({ commit }, value: string[]) {
      commit("descriptions", value)
    },
    fetch({ commit, getters }, { path, params = {} }: { path: string; params: Record<string, string | number> }) {
      commit("busy", +1)
      const { host, protocol } = window.location
      const url = new URL(`${protocol}//${host}/${getters.backend}${path}`)
      Object.entries(params).forEach(([key, val]) => url.searchParams.append(key, val))
      return fetch(url)
        .then(
          res => {
            if (res.ok) {
              return res.json()
            }
            throw new FetchError({ res, url })
          },
          err => {
            throw new FetchError({ err, url })
          },
        )
        .finally(() => {
          commit("busy", -1)
        })
    },
    get({ dispatch }, { pk }) {
      if (pk) {
        return dispatch("fetch", { path: `/positions/${pk}`, params: { md: false } }).then((res: Position) => {
          res.created_at = DateTime.fromFormat(<string>(<unknown>res.created_at), "EEE MMM d HH:m:s z yyyy")
          return res
        })
      }
      return null
    },
    list({ commit, dispatch, getters }, { description, location, page }) {
      if (page == 1) {
        commit("more", false)
        commit("positions", null)
      }
      if (getters.busy) {
        return getters.positions
      }
      if (description && location && (page == 1 || page === getters.page + 1)) {
        return dispatch("fetch", { path: "/positions", params: { description, location, page } }).then(
          (res: PositionListItem[]) => {
            res.forEach(rel => {
              rel.created_at = DateTime.fromFormat(<string>(<unknown>rel.created_at), "EEE MMM d HH:m:s z yyyy")
            })
            commit("more", res.length == 50 ? true : false)
            if (page > getters.page) {
              if (res.length > 0) {
                commit("positions", getters.positions.concat(res))
              }
            } else {
              commit("positions", res)
            }
            commit("page", page)
            return res
          },
        )
      }
      commit("more", false)
      commit("page", 1)
      commit("positions", null)
      return null
    },
    location({ commit, dispatch, getters: { description } }, location) {
      commit("location", location)
      return dispatch("list", { description, location, page: 1 })
    },
    locations({ commit }, value: string[]) {
      commit("locations", value)
    },
  },
  getters: {
    backend: state => state.backend,
    backends: state => state.backends,
    busy: state => (state.busy > 0 ? true : null),
    description: state => state.description,
    descriptions: state => state.descriptions,
    location: state => state.location,
    locations: state => state.locations,
    more: state => state.more,
    page: state => state.page,
    positions: state => state.positions,
  },
  mutations: {
    backend: (state, value) => (state.backend = value),
    busy: (state, value) => (state.busy += value),
    description: (state, value) => (state.description = value),
    descriptions: (state, value) => (state.descriptions = value),
    location: (state, value) => (state.location = value),
    locations: (state, value) => (state.locations = value),
    more: (state, value) => (state.more = value),
    page: (state, value) => (state.page = value),
    positions: (state, value) => (state.positions = value),
  },
  plugins: [],
  state: {
    backend: "conn/api/v1",
    backends: ["conn/api/v1", "djrf/api/v1"],
    busy: 0,
    description: null,
    descriptions: [],
    location: null,
    locations: [],
    more: false,
    page: 1,
    positions: null,
  },
  strict: true,
})

export function useStore() {
  return useStoreBase(key)
}

export interface State {
  backend: string
  backends: string[]
  busy: number
  description: string | null
  descriptions: string[]
  location: string | null
  locations: string[]
  more: boolean
  page: number
  positions: PositionListItem[] | null
}

interface PositionListItem {
  id: string
  type: string
  created_at: DateTime
  company: string
  location: string
  title: string
}

export interface Position {
  id: string
  type: string
  created_at: DateTime
  company: string
  company_url: string
  location: string
  title: string
  description: string
  how_to_apply: string
  company_logo: string | null
}
