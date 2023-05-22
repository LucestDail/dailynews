# Dailynews

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![](https://img.shields.io/badge/Maintained-yes-green.svg)
![](https://img.shields.io/website-up-down-green-red/http/monip.org.svg)
![](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)

![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![](https://img.shields.io/badge/mariaDB-003545?style=for-the-badge&logo=mariaDB&logoColor=white)
![](https://img.shields.io/badge/Amazon_AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![](https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white)
![](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

## 목차
[1. **프로젝트 소개**](#프로젝트-소개)

[2. **개발 환경**](#개발-환경)

[3. **설계 구조**](#설계-구조)

[4. **업데이트 진행**](#업데이트-진행)


## 프로젝트 소개
* 해당 프로젝트는 장고 기반 웹 어플리케이션이며, 다음 목표를 달성하기 위하여 제작되었습니다.  
  * 웹 상에 존재하는 뉴스나 커뮤니티 등 여러 웹 정보 종합 및 관리에 사용  
  * 업무 및 과제 수행에 종합적 정보 레포팅에 사용
  * 기타 소규모 팀 단위 업무 진행시 레포팅 및 리스크 관리에 사용  
* 개발 효율성을 향상시키기 위하여 다음과 같은 인프라가 활용, 구축되었습니다.  
  * Jenkins 및 Docker 를 이용한 CICD 파이프라인이 구성되었습니다.  
  * Amazon Web Service 환경을 이용한 클라우딩 기술을 활용하여 구축하였습니다.  
* 현재 프로젝트는 정상 배포중이며, 어플리케이션은 [다음 주소](https://dailydatahub.com/)를 통하여 접근이 가능합니다.  
  * 샘플 관리자 계정은 다음과 같습니다.  
    * ID:test
    * PW:test
* 해당 프로젝트는 [MIT 라이센스](https://choosealicense.com/licenses/mit/) 기반 배포 및 운영됩니다.  
  *  관련 의문사항이나 기타 2차 가공, 혹은 상업적 이용 등은 [이슈 생성](https://github.com/LucestDail/dailynews/issues)을 통하여 문의 및 진행하시길 바랍니다.



## 개발 환경

- 코드 작성 환경 구성
  * Pycharm
    * 파이썬 관리 및 가상 파이썬 환경에 적합한 에디트 툴 선택
  * DBeaver
    * Reference 다수 보유한 DB 에디트 툴 선택

- 어플리케이션 환경 구성
  * Python 3.9
    * Python 3 버전 중 프로젝트 진행 당시 가장 최근 버전을 선택
  * Django
    * 웹 프레임워크 초기 구축 효율화를 위해 Django 활용
  * pip
    * 빌드 툴 안정성 및 하위 호환성 pip 을 통한 라이브러리 관리
  * genism
    * TA 라이브러리 중 가장 레퍼런스가 많고 트위터에서 사용하는 genism 의 word2vec 활용 분석 실시
  * mariadb-java-client
    * Oracle 상업적 이용에 따른 유료 라이센스 상정, mysql 진영 무료 라이센스 데이터베이스 활용
    * Reference, Document 다수 보유한 MariaDB 선택
  
- 운영 환경 구성
  * aws cloudwatch
    * 어플리케이션 운영 환경에 대한 가비지 메모리, 현재 시스템 가용상태 확인을 위한 모니터링, 로깅 기능 도입
  * aws lambda
    * aws cloudwatch 연계 크롤링 데이터의 제약사항 극복(ip 차단 이슈)를 극복하기 위하여 동적 컴퓨팅 시도
    * AWS EC2 인스턴스를 활용하여 서버 구축 및 어플리케이션 배포 
      * Local 환경에서 구축시 상시 서버 기기 구동이 필요하므로 클라우드 서버로 대체
      * GCP, Heroku, Naver Cloud, Gabia 등 여러 서비스 확인하였으나,  
         실제 운영 서버 구축시 추가적으로 발생할 인프라 확장성을 고려 AWS 기반 인프라로 선택
    * Ubuntu 최신 버전을 활용하여 서버 보안성 향상 의도
    * DevOps 서버를 추가로 구성하여 해당 어플리케이션에 대한 모니터링, 자동 배포 기능을 수행  
      * 모니터링 서버, 자동 배포 서버 각각 구축 및 어플리케이션 포트 연동
  * jquery, jquery-ui,
    * 데이터 입력시에는 자체 비지니스 로직을 통한 데이터 입출입
  * gunicorn
    * 소규모 어플리케이션 구동시 가용성 및 추가적인 설정 고려 해당 gateway 선택

## 설계 구조
  * 기본적으로 AWS IaaS 기반으로 구성되며 이를 통하여 어플리케이션을 설정하였습니다.  
  * 어플리케이션 서버는 Micro 기반으로 구성, Devops 서버는 small 을 활용하여 구성하였습니다.(Docker 기반 빌드 시 가용성 고려)
  * AWS Route 53 을 활용한 DNS 도메인을 적용하였으며, 이를 활용하기 위하여 ELB 를 통한 라우팅 기능을 구성하였습니다.
  * HTTPS 적용시 현재 일부 기능 활용 및 호환이 제한되는 문제가 식별되어 HTTPS 를 HTTP 로 강제 라우팅 전환하여 서비스를 제공중입니다.
  * AWS RDS 를 활용하여 추가적인 용량 확보가 용이하도록 클라우딩 데이터베이스 기능을 구성하였습니다.
  * 내부적으로 MVC 구조를 채택하여 맵핑 후 RESTFul 한 서비스 URL 제공이 가능하도록 구성하였습니다.  
  * 서버에 접근 가능한 대상은 포트로 구분하여 AWS VPC 를 세팅, 구성하였습니다.  
  * 개발 가용성 및 배포 시간을 단축하기 위하여 Jenkins - Docker 기반 CICD Pipeline 이 구축되었습니다.

## 업데이트 진행
  - Ver 1.000(23.05.23)
    - README 최초 작성
      - 어플리케이션 소스코드 소개용도