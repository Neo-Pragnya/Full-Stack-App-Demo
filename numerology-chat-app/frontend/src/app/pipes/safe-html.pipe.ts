import { Pipe, PipeTransform } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';

@Pipe({
  name: 'safeHtml'
})
export class SafeHtmlPipe implements PipeTransform {
  constructor(private sanitizer: DomSanitizer) {}

  transform(value: string): SafeHtml {
    // Convert newlines to <br> tags and sanitize
    const htmlContent = value.replace(/\n/g, '<br>');
    return this.sanitizer.bypassSecurityTrustHtml(htmlContent);
  }
}