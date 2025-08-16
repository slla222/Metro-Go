plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
  signingConfigs {
    create("release") {
      storeFile = file(providers.gradleProperty("storeFile").getOrElse("upload-keystore.jks"))
      storePassword = providers.gradleProperty("MYAPP_UPLOAD_STORE_PASSWORD").getOrElse("android")
      keyAlias = providers.gradleProperty("MYAPP_UPLOAD_KEY_ALIAS").getOrElse("upload")
      keyPassword = providers.gradleProperty("MYAPP_UPLOAD_KEY_PASSWORD").getOrElse("android")
    }
  }
  buildTypes {
    release {
      signingConfig = signingConfigs.getByName("release")
    }
  }
  namespace = "com.example.metroalarm"
  compileSdk = 34

  defaultConfig {
    applicationId = "com.example.metroalarm"
    minSdk = 26
    targetSdk = 34
    versionCode = 1
    versionName = "1.0.0"
    vectorDrawables { useSupportLibrary = true }
  }

  buildTypes {
    release {
      isMinifyEnabled = false
      proguardFiles(
        getDefaultProguardFile("proguard-android-optimize.txt"),
        "proguard-rules.pro"
      )
    }
    debug { isMinifyEnabled = false }
  }

  buildFeatures { compose = true }
  composeOptions { kotlinCompilerExtensionVersion = "1.5.14" }
  packaging {
    resources.excludes += setOf(
      "META-INF/DEPENDENCIES",
      "META-INF/LICENSE",
      "META-INF/LICENSE.txt",
      "META-INF/NOTICE",
      "META-INF/NOTICE.txt"
    )
  }
}

dependencies {
  val composeBom = platform("androidx.compose:compose-bom:2024.06.00")
  implementation(composeBom)
  androidTestImplementation(composeBom)

  implementation("androidx.core:core-ktx:1.13.1")
  implementation("androidx.activity:activity-compose:1.9.0")
  implementation("androidx.compose.ui:ui")
  implementation("androidx.compose.material3:material3")
  implementation("androidx.navigation:navigation-compose:2.7.7")
  implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.4")
  implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.4")
  implementation("com.google.android.gms:play-services-location:21.3.0")
  implementation("com.google.android.play:billing-ktx:7.1.1")
  implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.8.1")
  implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.6.3")
  implementation("androidx.datastore:datastore-preferences:1.1.1")
  implementation("com.google.accompanist:accompanist-permissions:0.35.1-alpha")
  implementation("androidx.work:work-runtime-ktx:2.9.1")
  implementation("androidx.core:core-splashscreen:1.0.1")
  implementation("com.google.android.exoplayer:exoplayer:2.19.1")
  // SVG/Compose image loading
  implementation("io.coil-kt:coil-compose:2.6.0")
  implementation("io.coil-kt:coil-svg:2.6.0")
}

