pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = "{{APP_NAME}}"
include(
    ":app",
    ":core:common",
    ":core:designsystem",
    ":core:i18n",
    ":core:database",
    ":core:network",
    ":core:security",
    ":core:oem",
    ":feature:home",
    ":feature:settings",
    ":feature:premium",
)
