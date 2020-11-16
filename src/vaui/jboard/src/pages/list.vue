<template>
  <div class="aui-page-focused">
    <div id="page">
      <header id="header" role="banner">
        <nav class="aui-header">
          <div class="aui-header-inner">
            <div class="aui-header-primary">
              <span class="aui-header-logo aui-header-logo-textonly" />
            </div>
          </div>
        </nav>
      </header>
      <div id="content">
        <div class="aui-page-panel">
          <div class="aui-page-panel-inner">
            <section class="aui-page-panel-content">
              <div class="aui-message aui-message-error" v-if="error">
                <p class="title">
                  {{ error.name }}
                  <span class="aui-lozenge aui-lozenge-subtle aui-lozenge-error">{{ error.code }}</span>
                </p>
                <p class="title">{{ error.message }}</p>
                <small>{{ error.url }}</small>
              </div>
              <div v-else-if="!busy">
                <div class="aui-message aui-message-info" v-if="positions === null && (!description || !location)">
                  <p class="title">Welcome to DoneStreet Jobs Board!</p>
                  <p>Select:</p>
                  <ul>
                    <li v-if="!description">Programming Language</li>
                    <li v-if="!location">City</li>
                  </ul>
                </div>
                <div class="aui-message aui-message-warning" v-else-if="positions && positions.length === 0">
                  <p class="title">Nothing found!</p>
                  <p>Select another:</p>
                  <ul>
                    <li>Programming Language</li>
                    <li>City</li>
                  </ul>
                </div>
              </div>
              <div v-if="positions && positions.length > 0">
                <div class="aui-group aui-group-split" v-for="position in positions" :key="position.id">
                  <div class="aui-item">
                    <h4>
                      <router-link :to="{ name: 'detail', params: { pk: position.id } }">
                        {{ position.title }}
                      </router-link>
                    </h4>
                    <h6>
                      {{ position.company }} - <span>{{ position.type }}</span>
                    </h6>
                  </div>
                  <div class="aui-item">
                    <h5>{{ position.location }}</h5>
                    <h6>{{ position.created_at.toRelative() }}</h6>
                  </div>
                </div>
                <form class="aui top-label" v-if="more">
                  <div class="buttons-container">
                    <div class="buttons">
                      <v-aui-button :busy="busy" @click="search(description, location, page + 1)">
                        Load more
                      </v-aui-button>
                    </div>
                  </div>
                </form>
              </div>
            </section>
            <aside class="aui-page-panel-sidebar">
              <form class="aui top-label">
                <fieldset>
                  <div class="field-group">
                    <label>Programming Language<span class="aui-icon icon-required">required</span></label>
                    <v-aui-select v-model="description" :disabled="busy" :options="descriptions" />
                  </div>
                  <div class="field-group">
                    <label>City<span class="aui-icon icon-required">required</span></label>
                    <v-aui-select v-model="location" :disabled="busy" :options="locations" />
                  </div>
                  <div class="field-group">
                    <label>API Backend URL<span class="aui-icon icon-required">required</span></label>
                    <v-aui-select v-model="backend" :disabled="busy" :nullable="false" :options="backends" />
                    <div class="description" v-if="backend === 'djrf/api/v1'">
                      This backend ignore the <b>City</b>, so you test the pagination.
                    </div>
                  </div>
                </fieldset>
                <div class="buttons-container">
                  <div class="buttons">
                    <!-- prettier-ignore -->
                    <v-aui-button class="aui-button-primary" :busy="busy" :disabled="!description || !location"
                      @click="search(description, location, 1)">
                      Search
                    </v-aui-button>
                  </div>
                </div>
              </form>
            </aside>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { FetchError } from "../errors"
import { computed } from "vue"
import { defineComponent } from "vue"
import { ref } from "vue"
import { toRef } from "vue"
import { useStore } from "../store"

export default defineComponent({
  setup() {
    const error = ref<null | FetchError>()
    const store = useStore()
    const descriptions = toRef(store.getters, "descriptions")
    const locations = toRef(store.getters, "locations")

    if (!descriptions.value.length || !locations.value.length) {
      store.dispatch("fetch", { path: "/openapi.json" }).then(
        res => {
          res["paths"]["/positions"]["get"]["parameters"].forEach(
            ({ name, schema }: { name: string; schema: ParameterSchema }) => {
              if (name && schema.enum) {
                store.dispatch(`${name}s`, schema.enum)
              }
            },
          )
        },
        err => {
          error.value = err
          console.error(err)
        },
      )
    }

    return {
      backend: computed({
        get: () => store.getters.backend,
        set: value => {
          store.dispatch("backend", value).then(
            () => {
              error.value = null
            },
            err => {
              error.value = err
              console.error(err)
            },
          )
        },
      }),
      backends: toRef(store.getters, "backends"),
      busy: toRef(store.getters, "busy"),
      description: computed({
        get: () => store.getters.description,
        set: value => {
          store.dispatch("description", value).then(
            () => {
              error.value = null
            },
            err => {
              error.value = err
              console.error(err)
            },
          )
        },
      }),
      descriptions,
      error,
      location: computed({
        get: () => store.getters.location,
        set: value => {
          store.dispatch("location", value).then(
            () => {
              error.value = null
            },
            err => {
              error.value = err
              console.error(err)
            },
          )
        },
      }),
      locations,
      more: toRef(store.getters, "more"),
      page: toRef(store.getters, "page"),
      positions: toRef(store.getters, "positions"),
      search: (description: string, location: string, page: number) => {
        store.dispatch("list", { description, location, page }).then(
          () => {
            error.value = null
          },
          err => {
            error.value = err
            console.error(err)
          },
        )
      },
    }
  },
})

interface ParameterSchema {
  enum?: Array<string>
}
</script>

<style scoped>
.aui-button {
  padding: 4px 20px;
}
.aui-group {
  border-bottom: 1px solid #ddd;
  margin-top: 0;
  padding: 10px;
}
.aui-group > .aui-item + .aui-item {
  padding-left: 10px;
}
.aui-group .aui-item:first-child {
  width: 70%;
}
.aui-group .aui-item h4 {
  margin-top: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.aui-group .aui-item h5 {
  font-weight: normal;
  margin-top: 0;
}
.aui-group .aui-item h6 {
  color: #999;
  font-weight: normal;
  margin-top: 0;
}
.aui-group .aui-item h6 span {
  color: #1d9a00;
  font-weight: bold;
}
.aui-page-focused .aui-page-panel-content > form.aui .buttons-container {
  border-top: 0;
  margin-top: 0;
  padding-top: 0;
}
.buttons-container {
  text-align: center;
}
</style>
