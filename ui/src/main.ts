import { ApplicationConfig, bootstrapApplication } from '@angular/platform-browser';
import { ChatComponent } from './chat/chat.component';
import { provideHttpClient } from '@angular/common/http';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient()
  ]
};

bootstrapApplication(ChatComponent, appConfig)
  .catch(err => console.error(err));
